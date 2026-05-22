import bcrypt

def get_hashed_password(senha:str):
    senha_bytes = senha.encode('utf-8')

    salt = bcrypt.gensalt()
    senha_hashed = bcrypt.hashpw(senha_bytes, salt)

    return senha_hashed.decode('utf-8')
