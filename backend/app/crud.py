import secrets
import string
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from . import auth, models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    # Password validation
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_snippet(
    db: Session, snippet: schemas.SnippetCreate, user_id: int, encryption_service
):
    # Encrypt the code before storing
    encrypted_code = encryption_service.encrypt(snippet.code)

    db_snippet = models.Snippet(
        title=snippet.title,
        language=snippet.language,
        code=snippet.code,
        encrypted_code=encrypted_code,
        user_id=user_id,
    )
    db.add(db_snippet)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet


def get_user_snippets(db: Session, user_id: int):
    return db.query(models.Snippet).filter(models.Snippet.user_id == user_id).all()


def get_snippet_by_id(db: Session, snippet_id: int, user_id: int):
    return (
        db.query(models.Snippet)
        .filter(models.Snippet.id == snippet_id, models.Snippet.user_id == user_id)
        .first()
    )


def get_snippet_by_id_any_owner(db: Session, snippet_id: int):
    return db.query(models.Snippet).filter(models.Snippet.id == snippet_id).first()


def generate_share_token():
    """Generate a secure random token for sharing"""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(32))


def create_share_link(
    db: Session,
    snippet_id: int,
    user_id: int,
    expires_hours: int = 24,
    password: str = None,
):
    """Create a shareable link for a snippet"""
    # Verify the user owns the snippet
    snippet = get_snippet_by_id(db, snippet_id, user_id)
    if not snippet:
        return None

    token = generate_share_token()
    expires_at = (
        datetime.now(UTC) + timedelta(hours=expires_hours) if expires_hours else None
    )

    share_link = models.ShareLink(
        snippet_id=snippet_id,
        token=token,
        expires_at=expires_at,
        password_hash=auth.get_password_hash(password) if password else None,
        is_active=True,
    )
    db.add(share_link)
    db.commit()
    db.refresh(share_link)
    return share_link


def get_share_link_by_token(db: Session, token: str):
    """Get a share link by token, checking if it's valid"""
    share_link = (
        db.query(models.ShareLink)
        .filter(models.ShareLink.token == token, models.ShareLink.is_active)
        .first()
    )

    if not share_link:
        return None

    # Check if expired
    if share_link.expires_at:
        expires_at_aware = share_link.expires_at.replace(tzinfo=UTC)
        current_time_aware = datetime.now(UTC)

        if expires_at_aware < current_time_aware:
            share_link.is_active = False
            db.commit()
            return None

    return share_link


def verify_share_password(db: Session, share_link_id: int, password: str):
    """Verify password for a share link"""
    share_link = (
        db.query(models.ShareLink).filter(models.ShareLink.id == share_link_id).first()
    )
    if not share_link or not share_link.password_hash:
        return False

    return auth.verify_password(password, share_link.password_hash)


def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int = None,
    details: str = None,
):
    """Create an audit log entry"""
    audit_log = models.AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
    )
    db.add(audit_log)
    db.commit()
    return audit_log
