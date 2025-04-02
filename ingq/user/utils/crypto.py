from cryptography.fernet import Fernet
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()


class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        key = os.getenv("ENCRYPTION_KEY")
        self.fernet = Fernet(key)

    def encrypt(self, secret):
        return self.pwd_context.hash(secret)

    def verify(self, secret, hash):
        return self.pwd_context.verify(secret, hash)

    def phone_encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def phone_decrypt(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
