import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

    # Encryption
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY")

    def validate(self):
        """Validate that all required environment variables are set"""
        required_vars = {
            "DATABASE_URL": self.DATABASE_URL,
            "SECRET_KEY": self.SECRET_KEY,
            "JWT_SECRET_KEY": self.JWT_SECRET_KEY,
            "ENCRYPTION": self.ENCRYPTION_KEY,
        }

        missing_vars = [var for var,
                        value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        # Validate encryption key length
        if self.ENCRYPTION_KEY and len(self.ENCRYPTION_KEY) != 32:
            raise ValueError(
                "ENCRYPTION_KEY must be exactly 32 characters long")


# Create global settings instance
settings = Settings()
