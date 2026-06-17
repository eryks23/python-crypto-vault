# vault_engine — AES-256 Local Encryption Vault

> Encrypt and decrypt sensitive strings locally from the terminal — no cloud, no logs, no leaks.

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [Description](#description)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Author](#author)

---

## Description

`vault_engine` is a terminal-based encryption utility that encrypts and decrypts arbitrary text strings using AES-256-CFB with a PBKDF2-derived key. Every encryption call generates a fresh random salt and IV, so ciphertext is non-deterministic even for identical inputs. It targets developers and power users who need quick, offline encryption without relying on third-party services or cloud storage.

---

## Key Features

- **AES-256-CFB encryption** — strong symmetric cipher with a 256-bit key derived from your master password
- **PBKDF2-HMAC-SHA256 key derivation** — 100,000 iterations harden the key against brute-force and dictionary attacks
- **Per-call random salt and IV** — each vault string is unique, even when encrypting the same plaintext twice
- **Self-contained base64 output** — the encrypted blob bundles salt + IV + ciphertext; safe to copy, paste, or store anywhere
- **Zero external data transfer** — runs entirely offline; nothing is logged, transmitted, or persisted
- **Cross-platform** — works on Windows, macOS, and Linux with no platform-specific dependencies

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.7+ |
| Encryption | AES-256-CFB |
| Key derivation | PBKDF2-HMAC-SHA256 |
| Crypto backend | [`cryptography`](https://cryptography.io) (PyCA) |
| Interface | Interactive terminal CLI |

---

## Requirements

- Python **3.7** or higher
- pip

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/eryks23/python-crypto-vault
cd python-crypto-vault

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python vault_engine.py
```

The CLI presents three operations after you supply your master password:

| Option | Action |
|---|---|
| `1` | Encrypt a plaintext string → returns a base64 vault string |
| `2` | Decrypt a vault string → returns the original plaintext |
| `3` | Exit |

**Example session:**

```
============================================================
  LOCAL CRYPTO VAULT | AES-256 SECURE STORAGE
  System Status: Active | Encryption: Enabled
============================================================

[>] Master Password:

[1] Encrypt data
[2] Decrypt data
[3] Exit

Select: 1
Input string: my secret message

VAULT STRING:
dGhpcyBpcyBhIGV4YW1wbGUgb3V0cHV0IGZvciBkb2Nz...

Select: 2
Paste string: dGhpcyBpcyBhIGV4YW1wbGUgb3V0cHV0IGZvciBkb2Nz...

RESULT:
my secret message
```

> **Important:** You must use the same master password for both encryption and decryption. There is no password recovery mechanism — a wrong password produces garbled output or an `[ERROR]` message.

---

## API Reference

`CryptoEngine` can also be imported directly for programmatic use.

### `CryptoEngine(password: str)`

Instantiates the encryption engine.

| Parameter | Type | Description |
|---|---|---|
| `password` | `str` | Master password used to derive the AES key via PBKDF2 |

```python
from vault_engine import CryptoEngine

vault = CryptoEngine(password="your-master-password")
```

---

### `encrypt(plaintext: str) -> str`

Encrypts a string and returns a portable, base64-encoded vault token.

| Parameter | Type | Description |
|---|---|---|
| `plaintext` | `str` | The string to encrypt |

**Returns:** A base64 string encoding `salt[16 bytes] + iv[16 bytes] + ciphertext`.

```python
token = vault.encrypt("sensitive data")
print(token)
# e.g. "dGhpcyBpcyBhIGZha2UgZW5jcnlwdGVkIG91dHB1dA=="
```

---

### `decrypt(encrypted_data: str) -> str`

Decrypts a vault token produced by `encrypt()`.

| Parameter | Type | Description |
|---|---|---|
| `encrypted_data` | `str` | Base64 string produced by `encrypt()` |

**Returns:** Original plaintext string on success. Returns a string prefixed with `[ERROR]` on failure — for example, when a wrong password or malformed token is supplied — instead of raising an exception.

```python
result = vault.decrypt(token)
print(result)
# "sensitive data"
```

---

### Encryption parameters reference

| Parameter | Value |
|---|---|
| Algorithm | AES-256-CFB |
| Key size | 32 bytes (256 bits) |
| KDF | PBKDF2-HMAC-SHA256 |
| KDF iterations | 100,000 |
| Salt | 16 bytes, random per call (`os.urandom`) |
| IV | 16 bytes, random per call (`os.urandom`) |

---

## Project Structure

```
python-crypto-vault/
├── vault_engine.py     # CryptoEngine class + interactive CLI entry point
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Testing

The project does not yet include an automated test suite. To verify round-trip correctness manually:

```python
from vault_engine import CryptoEngine

engine = CryptoEngine("test-password")
original = "hello world"

encrypted = engine.encrypt(original)
decrypted = engine.decrypt(encrypted)

assert decrypted == original, f"Round-trip failed: got '{decrypted}'"
print("Round-trip OK.")
```

To run tests once a suite is added:

```bash
pip install pytest
pytest
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit with a descriptive message: `git commit -m "Add: description of change"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request against `main`

Keep each PR focused on a single concern. If you're adding new encryption modes or KDF options, include a usage example in the PR description.

---

## Author

**eryks23**  
GitHub: [@eryks23](https://github.com/eryks23)  
Repository: [https://github.com/eryks23/python-crypto-vault](https://github.com/eryks23/python-crypto-vault)

---

> **Security note:** `vault_engine` is intended for personal, local use. For production secrets management consider a dedicated solution such as [HashiCorp Vault](https://www.vaultproject.io/), [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), or [Bitwarden](https://bitwarden.com/).
