🛡️ SecureVault
Password-based file encryption tool written in Python.

SecureVault provides secure encryption and decryption of files and directories using modern cryptographic standards and clean architectural principles. It is a portfolio-level project designed to demonstrate secure coding practices, separation of concerns, and production-style structure.

🚀 Key Features
Strong Encryption: Uses AES-based symmetric encryption via Fernet.

Secure Key Derivation: Implements PBKDF2 with SHA-256 and 200,000 iterations.

Unique Salts: Every file gets a unique 16-byte cryptographically secure salt.

Tamper Detection: Authenticated encryption ensures that any modification to the encrypted file is detected.

Recursive Directory Support: Easily encrypt/decrypt entire folder structures.

CLI Interface: Clean and intuitive command-line interaction with secure password input.

🛠️ Security Design
SecureVault follows a "Security by Design" approach:

Key Derivation: Instead of using the password directly, we derive a key using PBKDF2HMAC. This prevents rainbow table attacks.

Unique Keys per File: By storing a unique salt at the beginning of each .enc file, the same password produces a different key for every file.

Integrity Checks: Using Fernet ensures that if even a single bit of the encrypted file is changed, the decryption will fail with an explicit error instead of returning corrupted data.

📂 Project Structure
The project follows a Clean Architecture model, separating business logic from the interface:

vault.py: Core cryptographic engine and business logic.

cli.py: User interaction layer and argument parsing.

tests/: Automated test suite using pytest.

💻 Installation & Usage
Setup
Bash

git clone https://github.com/yourusername/SecureVault.git
cd SecureVault
pip install -r requirements.txt
Encrypt a file
Bash

python cli.py encrypt my_data.txt
Decrypt a directory
Bash

python cli.py decrypt ./my_encrypted_folder
🧪 Testing
The project includes a comprehensive test suite. To run tests:

Bash

pytest tests/
Tests are executed in isolated temporary directories to ensure environment safety.

⚠️ Disclaimer
This project is intended for educational and portfolio purposes. Although it uses industry-standard cryptographic primitives, it has not undergone a formal security audit.
