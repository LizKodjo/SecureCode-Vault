import pytest
from app.encryption import EncryptionService


def test_encryption_service():
    """Test encryption and decryption functionality"""
    encryption_service = EncryptionService()

    # Test basic encryption/decryption
    original_text = "This is a secret message"
    encrypted = encryption_service.encrypt(original_text)
    decrypted = encryption_service.decrypt(encrypted)

    assert decrypted == original_text
    assert encrypted != original_text

    # Test different content
    another_text = "Another secret"
    another_encrypted = encryption_service.encrypt(another_text)

    assert another_encrypted != encrypted

    # Test empty string
    empty_encrypted = encryption_service.encrypt("")
    empty_decrypted = encryption_service.decrypt(empty_encrypted)
    assert empty_decrypted == ""


def test_encryption_consistency():
    """Test that same input produces different output (due to salting)"""
    encryption_service = EncryptionService()
    text = "Same text"

    encrypted1 = encryption_service.encrypt(text)
    encrypted2 = encryption_service.encrypt(text)

    # Should be different due to random salt
    assert encrypted1 != encrypted2

    # But both should decrypt to the same text
    assert encryption_service.decrypt(encrypted1) == text
    assert encryption_service.decrypt(encrypted2) == text
