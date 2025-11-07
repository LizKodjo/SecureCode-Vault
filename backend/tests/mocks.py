"""
Mock services for testing
"""


class MockEncryptionService:
    """Mock encryption service that doesn't actually encrypt for testing"""

    def __init__(self):
        print("🔧 Using mock encryption service for testing")

    def encrypt(self, data: str) -> str:
        """Mock encryption - returns a predictable 'encrypted' version"""
        # For testing, we need this to be reversible
        return f"mock_encrypted:{data}"

    def decrypt(self, encrypted_data: str) -> str:
        """Mock decryption - reverses the mock encryption"""
        if encrypted_data.startswith("mock_encrypted:"):
            return encrypted_data[15:]  # Remove the prefix
        # If it's not our mock format, return as-is (for already encrypted data)
        return encrypted_data


# Global mock encryption service
mock_encryption_service = MockEncryptionService()
