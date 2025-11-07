import base64

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
            raise ValueError("ENCRYPTION_KEY must be exactly 32 characters long")

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
except ValueError as e:
    print(f"⚠️ Encryption service initialisation failed: {e}")
    print(
        f"⚠️ Encryption will not be available . Set ENCRYPTION_KEY environment variable."
    )
    encryption_service = None
