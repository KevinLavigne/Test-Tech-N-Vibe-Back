import os
import jwt

def Decode_auth_token(token):

    decoded_data = jwt.decode(jwt=token,
      key= os.getenv('SECRET_KEY'),
      algorithms=["HS256"])

    if decoded_data :
      return True
    return False