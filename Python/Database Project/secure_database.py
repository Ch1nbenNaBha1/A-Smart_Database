import os
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class SecureDatabase:
    def __init__(self, db_file="secure_data.db", key_file="db_key.key"):
        self.db_file = db_file
        self.key_file = key_file
        self.user_data = {}
        self.key = self._load_or_create_key()
        self._load_database()

    # Encryption helpers
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        key = get_random_bytes(16)
        with open(self.key_file, "wb") as f:
            f.write(key)
        return key

    def _encrypt_data(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        return (bytes(cipher.iv) + ct_bytes).hex()

    def _decrypt_data(self, encrypted_hex: str) -> str:
        encrypted_data = bytes.fromhex(encrypted_hex)
        iv = encrypted_data[:AES.block_size]
        ct = encrypted_data[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    # CRUD Methods (updated names to match Flask)
    def add_record(self, record_id: str, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        self.user_data[record_id] = self._encrypt_data(data)
        self._save_database()

    def get_record(self, record_id: str):
        if record_id not in self.user_data:
            return None
        decrypted = self._decrypt_data(self.user_data[record_id])
        try:
            return json.loads(decrypted)
        except json.JSONDecodeError:
            return decrypted

    def delete_record(self, record_id: str):
        if record_id in self.user_data:
            del self.user_data[record_id]
            self._save_database()
            return True
        return False

    def get_all(self):
        """Return list of (id, data) tuples"""
        return [(rid, self.get_record(rid)) for rid in self.user_data]


    # Persistence
    def _save_database(self):
        with open(self.db_file, "w") as f:
            json.dump(self.user_data, f)

    def _load_database(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                self.user_data = json.load(f)

    # Utility
    def clear(self):
        self.user_data = {}
        self._save_database()
