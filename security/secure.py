from jose import jwt
import os

class Authorization:
    def __init__(self):
        self._SECRET_KEY:str = os.getenv('API_SECRET') if os.getenv('API_SECRET') is not None else 'estro'
        self._ALGORITHM:str = 'HS256'
        self._PASS:str = os.getenv('API_PASSWORD')
        self._username:str

    def set_cred(self, token:str) -> bool:
        payload = jwt.decode(token, key=self._SECRET_KEY, algorithms=self._ALGORITHM)
        self.username = payload.get('username')
        self.password = payload.get('password')