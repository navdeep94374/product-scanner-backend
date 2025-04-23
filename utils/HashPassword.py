import bcrypt

class HashPassword:
    def hashPwd(password:str):
        salt = bcrypt.gensalt() 
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed
    
    def verifyPwd(plain_pwd,hashed_pwd):
        result = bcrypt.checkpw(plain_pwd.encode('utf-8'), hashed_pwd)
        return result
