import base64
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .config import settings


class EncryptionService:
    def __init__(self):
        # Check if encryption key is available
        if not settings.ENCRYPTION_KEY:
            raise ValueError("ENCRYPTION_KEY environment variable is not set")

        # Validate encryption key length
        if len(settings.ENCRYPTION_KEY) != 32:
            raise ValueError(
                f"ENCRYPTION_KEY must be exactly 32 characters long got {len(settings.ENCRYPTION_KEY)}"
            )

        # Derive a Fernet key from our encryption key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"securecode_vault_salt",
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(settings.ENCRYPTION_KEY.encode()))
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        encrypted_data = self.fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.fernet.decrypt(encrypted_bytes)
        return decrypted_data.decode()


# Global encryption service instance - handle initialisation gracefully
try:
    encryption_service = EncryptionService()
    print("✅ Encryption service initialised successfully")
except ValueError as e:
    print(f"⚠️ Encryption service initialisation failed: {e}")
    # Create mock service for testing
    if "test" in str(settings.DATABASE_URL).lower() or "pytest" in sys.modules:
        print("⚠️ Creating mock encryption service for testing.")
        encryption_service = None
    else:
        encryption_service = None
