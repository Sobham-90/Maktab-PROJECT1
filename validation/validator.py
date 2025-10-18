import re

def username_validator(username):
    pattern = r"^[a-zA-Z0-9]{5,15}$"
    return re.match(pattern, username) is not None

def password_validator(password):
    pattern = r"^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$"
    return re.match(pattern, password) is not None