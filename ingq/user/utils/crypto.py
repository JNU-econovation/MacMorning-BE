from cryptography.fernet import Fernet
from passlib.context import CryptContext

from core.setting.load_env import ENCRYPTION_KEY


class Crypto:
    def __init__(self):
        # Password Encrypt
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # Phone Number Encrypt & Decrypt
        key = ENCRYPTION_KEY
        self.fernet = Fernet(key)

    def encrypt(self, secret):
        return self.pwd_context.hash(secret)

    def verify(self, secret, hash):
        return self.pwd_context.verify(secret, hash)

    def phone_encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def phone_decrypt(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
