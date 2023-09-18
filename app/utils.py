from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed(password):
    return pwd_context.hash(password)


def is_valid(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
