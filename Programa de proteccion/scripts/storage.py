import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROTECTION_FOLDER

if not os.path.exists(PROTECTION_FOLDER):
    os.makedirs(PROTECTION_FOLDER)

PASSWORD_FILE = os.path.join(PROTECTION_FOLDER, "password.txt")


def password_exists():
    return os.path.exists(PASSWORD_FILE)


def save_password(password):
    with open(PASSWORD_FILE, "w") as file:
        file.write(password)


def load_password():
    with open(PASSWORD_FILE, "r") as file:
        return file.read()