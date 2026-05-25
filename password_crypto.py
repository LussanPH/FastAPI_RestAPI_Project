import bcrypt

def get_hashed_password(senha:str):
    senha_bytes = senha.encode('utf-8')

    salt = bcrypt.gensalt()
    senha_hashed = bcrypt.hashpw(senha_bytes, salt)

    return senha_hashed.decode('utf-8')

def verify_password(senha_login:str, sennha_criptografada_db:str):
    senha_login_bytes = senha_login.encode('utf-8')
    sennha_criptografada_db_bytes = sennha_criptografada_db.encode('utf-8')

    return bcrypt.checkpw(senha_login_bytes, sennha_criptografada_db_bytes)