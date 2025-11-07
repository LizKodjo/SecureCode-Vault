"""
Mock services for testing
"""


class MockEncryptionService:
    """Mock encryption service that doesn't actually encrypt for testing"""

    def __init__(self):
        print("🔧 Using mock encryption service for testing")

    def encrypt(self, data: str) -> str:
        """Mock encryption - just returns the data with 'encrypted:' prefix"""
        return f"encrypted:{data}"

    def decrypt(self, encrypted_data: str) -> str:
        """Mock decryption - removes the 'encrypted:' prefix"""
        if encrypted_data.startswith("encrypted:"):
            return encrypted_data[10:]
        return encrypted_data


# Global mock encryption service
mock_encryption_service = MockEncryptionService()
