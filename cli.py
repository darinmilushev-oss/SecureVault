import argparse
from pathlib import Path
from getpass import getpass

from vault import SecureVault


def main():
    parser = argparse.ArgumentParser(
        description="SecureVault - Password-based file encryption tool"
    )

    parser.add_argument("action", choices=["encrypt", "decrypt"])
    parser.add_argument("target")

    args = parser.parse_args()

    password = getpass("Enter password (min 8 chars): ")

    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return

    vault = SecureVault()
    target_path = Path(args.target)

    if not target_path.exists():
        print("Target not found.")
        return

    try:
        if args.action == "encrypt":
            if target_path.is_file():
                result = vault.encrypt_file(target_path, password)
                print(f"Encrypted: {result}")
            else:
                vault.encrypt_directory(target_path, password)
                print("Directory encrypted.")

        else:
            if target_path.is_file():
                result = vault.decrypt_file(target_path, password)
                print(f"Decrypted: {result}")
            else:
                vault.decrypt_directory(target_path, password)
                print("Directory decrypted.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()