import bcrypt


def verify_password(plain_password: str, php_bcrypt_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), php_bcrypt_hash.encode())


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
