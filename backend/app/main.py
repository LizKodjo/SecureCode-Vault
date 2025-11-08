from datetime import UTC, datetime

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import auth, crud, models, schemas
from .config import settings
from .database import SessionLocal, engine, get_db
from .encryption import encryption_service
from .middleware import audit_middleware

try:
    settings.validate()
    print("✅ All environment variables are properly configured")
except ValueError as e:
    print(f"❌ Configuration error: {e}")

if encryption_service is None:
    print("❌ Encryption service is not available - encryption/decryption will fail")
else:
    print("✅ Encryption service is available")

    # Add tags for better organization
tags_metadata = [
    {
        "name": "authentication",
        "description": "User registration and login endpoints",
    },
    {
        "name": "snippets",
        "description": "Create and manage code snippets",
    },
    {
        "name": "sharing",
        "description": "Generate and access shared snippets",
    },
    {
        "name": "users",
        "description": "User profile management",
    },
    {
        "name": "health",
        "description": "Health checks and service status",
    },
]


# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureCode Vault API",
    description="""
    🔒 SecureCode Vault - A secure platform for code snippet management.
    
    ## Features
    
    * **User Authentication** - JWT token-based auth
    * **Encrypted Storage** - Code snippets encrypted at rest
    * **Secure Sharing** - Expiring, password-protected share links
    * **Audit Logging** - Comprehensive activity tracking
    
    ## Endpoints
    
    * **Auth** - User registration and login
    * **Snippets** - Create, read, and manage code snippets  
    * **Sharing** - Generate and access shared snippets
    * **Users** - User profile management
    """,
    version="1.0.0",
    contact={
        "name": "Liz Kodjo",
        "url": "https://github.com/LizKodjo/SecureCode-Vault",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
)


# Add audit middleware


@app.middleware("http")
async def add_audit_middleware(request: Request, call_next):
    return await audit_middleware(request, call_next)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://127.0.0.1:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to SecureCode Vault API"}


@app.get("/health", tags=["health"])
async def health_check():
    """Enhanced health check that verifies all services"""
    try:
        # Test database connection
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        # Test encryption service
        encryption_status = "unavailable"
        if encryption_service:
            test_data = "health_check"
            encrypted = encryption_service.encrypt(test_data)
            decrypted = encryption_service.decrypt(encrypted)

            if decrypted != test_data:
                raise Exception("Encryption service test failed")
            encryption_status = "working"

            return {
                "status": "healthy",
                "database": "connected",
                "encryption": encryption_status,
                "timestamp": datetime.now(UTC).isoformat(),
            }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Service unhealthy: {str(e)}"
        ) from None


@app.get("/test/encryption")
async def test_encryption():
    """Test endpoint to verify encryption is working"""
    try:
        test_data = "Hello, SecureCode Vault"
        encrypted = encryption_service.encrypt(test_data)
        decrypted = encryption_service.decrypt(encrypted)

        return {
            "original": test_data,
            "encrypted": encrypted,
            "decrypted": decrypted,
            "success": decrypted == test_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Encryption test failed: {str(e)}"
        ) from None


# Authenticate endpoints


@app.post("/auth/register", response_model=schemas.UserResponse, tags=["authentication"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        new_user = crud.create_user(db=db, user=user)
        # Log the registration
        crud.create_audit_log(db, new_user.id, "REGISTER",
                              "USER", new_user.id, "User registered")

        # Commit the transaction explicitly
        db.commit()

        # Refresh to get the complete user object
        db.refresh(new_user)
        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@app.post("/auth/login", response_model=schemas.Token, tags=["authentication"])
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    # Log the login
    crud.create_audit_log(db, user.id, "LOGIN", "USER",
                          user.id, "User logged in")
    return {"access_token": access_token, "token_type": "bearer"}


# Protected endpoints
@app.post("/snippets", response_model=schemas.SnippetResponse, tags=["snippets"])
def create_snippet(
    snippet: schemas.SnippetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_snippet = crud.create_snippet(
        db=db,
        snippet=snippet,
        user_id=current_user.id,
        encryption_service=encryption_service,
    )
    # Log snippet creation
    crud.create_audit_log(
        db,
        current_user.id,
        "CREATE",
        "SNIPPET",
        new_snippet.id,
        f"Snippet created: {snippet.title}",
    )
    return new_snippet


@app.get("/snippets", response_model=list[schemas.SnippetResponse], tags=["snippets"])
def get_my_snippets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # Get user's snippets
    snippets = crud.get_user_snippets(db, user_id=current_user.id)
    # Log snippet access
    crud.create_audit_log(
        db, current_user.id, "READ", "SNIPPET", None, "Accessed snippets list"
    )
    return snippets


@app.get("/snippets/{snippet_id}", response_model=schemas.SnippetResponse)
def get_snippet(
    snippet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    snippet = crud.get_snippet_by_id(db, snippet_id, current_user.id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    # Log specific snippet access
    crud.create_audit_log(
        db, current_user.id, "READ", "SNIPPET", snippet_id, f"Accessed: {snippet.title}"
    )
    return snippet


@app.delete("/snippets/{snippet_id}")
def delete_snippet(
    snippet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    snippet = crud.get_snippet_by_id(db, snippet_id, current_user.id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    db.delete(snippet)
    db.commit()
    # Log snippet deletion
    crud.create_audit_log(
        db,
        current_user.id,
        "DELETE",
        "SNIPPET",
        snippet_id,
        f"Deleted snippet: {snippet.title}",
    )
    return {"message": "Snippet deleted successfully"}


# Share endpoints


@app.post("/snippets/{snippet_id}/share", response_model=schemas.ShareLinkResponse, tags=["sharing"])
def create_share_link(
    snippet_id: int,
    share_data: schemas.ShareLinkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    share_link = crud.create_share_link(
        db=db,
        snippet_id=snippet_id,
        user_id=current_user.id,
        expires_hours=share_data.expires_hours,
        password=share_data.password,
    )

    if not share_link:
        raise HTTPException(
            status_code=404, detail="Snippet not found or access denied"
        )

    # Log share creation
    crud.create_audit_log(
        db,
        current_user.id,
        "SHARE",
        "SNIPPET",
        snippet_id,
        f"Created share link for snippet: {share_link.token}",
    )

    return share_link


@app.get("/shared/{token}", response_model=schemas.SharedSnippetResponse, tags=["sharing"])
def access_shared_snippet(
    token: str,
    access_data: schemas.ShareAccessRequest | None = None,
    db: Session = Depends(get_db),
):
    share_link = crud.get_share_link_by_token(db, token)
    if not share_link:
        raise HTTPException(
            status_code=404, detail="Shared link not found or expired")

    # Check password is required
    if share_link.password_hash:
        if not access_data or not access_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password required to access this shared snippet",
            )

        if not crud.verify_share_password(db, share_link.id, access_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )

    snippet = crud.get_snippet_by_id_any_owner(db, share_link.snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")

    # Decrypt the code
    try:
        if encryption_service:
            decrypted_code = encryption_service.decrypt(snippet.encrypted_code)
        else:
            # For testing, handle mock encryption
            if snippet.encrypted_code.startswith("mock_encrypted:"):
                decrypted_code = snippet.encrypted_code[15:]
            else:
                decrypted_code = snippet.code
    except Exception as e:
        print(f"Decryption error: {e}")
        # Fallback
        decrypted_code = snippet.code

    # Log shared access (anonymous)
    crud.create_audit_log(
        db,
        None,
        "SHARED_ACCESS",
        "SNIPPET",
        snippet.id,
        f"Anonymous access via token: {token}",
    )

    return schemas.SharedSnippetResponse(
        title=snippet.title,
        language=snippet.language,
        code=decrypted_code,
        shared_at=share_link.created_at,
    )


@app.get("/users/me", response_model=schemas.UserResponse, tags=["users"])
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
