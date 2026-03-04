import pytest
from pathlib import Path
from vault import SecureVault


@pytest.fixture
def vault():
    return SecureVault()


@pytest.fixture
def password():
    return "StrongPassword123!"


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("This is a test file.")
    return file_path


def test_encrypt_creates_file(vault, sample_file, password):
    encrypted_path = vault.encrypt_file(sample_file, password)
    assert encrypted_path.exists()


def test_encryption_changes_content(vault, sample_file, password):
    original = sample_file.read_bytes()
    encrypted_path = vault.encrypt_file(sample_file, password)
    encrypted = encrypted_path.read_bytes()

    assert original != encrypted


def test_decrypt_restores_content(vault, sample_file, password):
    original = sample_file.read_bytes()
    encrypted_path = vault.encrypt_file(sample_file, password)
    decrypted_path = vault.decrypt_file(encrypted_path, password)

    assert decrypted_path.read_bytes() == original


def test_wrong_password_raises(vault, sample_file, password):
    encrypted_path = vault.encrypt_file(sample_file, password)

    with pytest.raises(ValueError):
        vault.decrypt_file(encrypted_path, "WrongPassword!")


def test_nonexistent_file(vault):
    with pytest.raises(FileNotFoundError):
        vault.encrypt_file(Path("fake.txt"), "pass123456")