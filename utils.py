import logging
from cryptography.fernet import Fernet

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        filename='stripe_tool.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def encrypt_data(data, key):
    """Encrypt sensitive data using Fernet symmetric encryption."""
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    """Decrypt sensitive data."""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
