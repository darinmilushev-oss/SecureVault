import os
import base64
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 16
ITERATIONS = 200_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a secure key from password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


class SecureVault:
    """Password-based file encryption tool."""

    def encrypt_file(self, file_path: Path, password: str) -> Path:
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found.")

        salt = os.urandom(SALT_SIZE)
        key = derive_key(password, salt)
        fernet = Fernet(key)

        data = file_path.read_bytes()
        encrypted = fernet.encrypt(data)

        output_path = file_path.with_suffix(file_path.suffix + ".enc")
        output_path.write_bytes(salt + encrypted)

        return output_path

    def decrypt_file(self, file_path: Path, password: str) -> Path:
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found.")

        data = file_path.read_bytes()

        salt = data[:SALT_SIZE]
        encrypted = data[SALT_SIZE:]

        key = derive_key(password, salt)
        fernet = Fernet(key)

        try:
            decrypted = fernet.decrypt(encrypted)
        except InvalidToken:
            raise ValueError("Wrong password or corrupted file.")

        output_path = file_path.with_suffix("").with_suffix(".dec")
        output_path.write_bytes(decrypted)

        return output_path

    def encrypt_directory(self, folder: Path, password: str):
        for file in folder.rglob("*"):
            if file.is_file():
                self.encrypt_file(file, password)

    def decrypt_directory(self, folder: Path, password: str):
        for file in folder.rglob("*.enc"):
            if file.is_file():
                self.decrypt_file(file, password)

        
 