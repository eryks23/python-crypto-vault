import os
import base64
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CryptoEngine:
    
    def __init__(self, password: str):
        self.password = password.encode()
        self.backend = default_backend()
        self.iterations = 100_000

    def _generate_key(self, salt: bytes) -> bytes:

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )

        return kdf.derive(self.password)

    def encrypt(self, plaintext: str) -> str:

        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._generate_key(salt)
        
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        
        combined = salt + iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:

        try:
            decoded = base64.b64decode(encrypted_data)
            salt = decoded[:16]
            iv = decoded[16:32]
            ciphertext = decoded[32:]
            
            key = self._generate_key(salt)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
            decryptor = cipher.decryptor()

            return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
        
        except Exception as e:
            return f"[ERROR] Failed to decrypt: {e}!"

def display_ui():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[94m" + "="*60)
    print("  LOCAL CRYPTO VAULT | AES-256 SECURE STORAGE")
    print("  System Status: Active | Encryption: Enabled")
    print("="*60 + "\033[0m")

def main():
    display_ui()
    
    print(f"[*] Booting encryption modules...")
    time.sleep(0.5)
    
    master_pass = input("[>] Master Password: ")
    vault = CryptoEngine(master_pass)
    
    while True:
        print("\n\033[92m[1] Encrypt data")
        print("[2] Decrypt data")
        print("[3] Exit\033[0m")
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            msg = input("Input string: ")
            encrypted = vault.encrypt(msg)
            print(f"\n\033[93mVAULT STRING:\033[0m\n{encrypted}")
        
        elif choice == "2":
            data = input("Paste string: ")
            decrypted = vault.decrypt(data)
            print(f"\n\033[92mRESULT:\033[0m\n{decrypted}")
            
        elif choice == "3":
            print("Session terminated. Security locks engaged!")
            break
        else:
            print("Unknown command!")

if __name__ == "__main__":
    main()