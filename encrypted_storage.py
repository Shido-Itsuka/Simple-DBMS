import os
import json
import base64
import shutil
from cryptography.fernet import Fernet


class EncryptedStorage:
    def __init__(self, folder_name=".secure_data"):
        """
        Инициализация хранилища.
        :param folder_name: Имя скрытой папки для хранения данных.
        """
        self.base_path = os.path.join(os.getcwd(), folder_name)
        self.key_path = os.path.join(self.base_path, "key.key")
        self.data_path = os.path.join(self.base_path, "data.enc")

        # Создание скрытой папки, если её нет
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            self._hide_folder()

        # Генерация ключа, если он отсутствует
        if not os.path.exists(self.key_path):
            self._generate_key()

        # Загрузка ключа
        self.cipher = Fernet(self._load_key())

    def _hide_folder(self):
        """Скрывает папку в Windows."""
        if os.name == "nt":  # Windows
            os.system(f'attrib +h "{self.base_path}"')

    def _generate_key(self):
        """Генерирует и сохраняет ключ шифрования."""
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as key_file:
            key_file.write(key)

    def _load_key(self):
        """Загружает ключ шифрования из файла."""
        with open(self.key_path, "rb") as key_file:
            return key_file.read()

    def save_data(self, data: dict):
        """
        Сохраняет зашифрованные данные в файл.
        :param data: Данные в формате словаря.
        """
        json_data = json.dumps(data).encode()
        encrypted_data = self.cipher.encrypt(json_data)
        with open(self.data_path, "wb") as data_file:
            data_file.write(encrypted_data)

    def load_data(self):
        """
        Загружает и расшифровывает данные из файла.
        :return: Данные в формате словаря.
        """
        if not os.path.exists(self.data_path):
            return {}

        with open(self.data_path, "rb") as data_file:
            encrypted_data = data_file.read()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())

    def delete_storage(self):
        """
        Удаляет папку с ключом и зашифрованными данными.
        """
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)
            print(f"Папка {self.base_path} успешно удалена.")
