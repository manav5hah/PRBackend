from typing import Optional, Union
from pydantic import BaseModel, Field

class UserClientCode(BaseModel):
    client_id: Optional[str] = Field(title="The client id", pattern=r'[A-Za-z]\d{3,4}')
    
class UserMCap(BaseModel):
    client_code: Optional[str] = Field(default=None, title="The 8 digit client code", pattern=r'[0-9]{8}')
    family_code: Optional[str] = Field(default=None, title="The family code", pattern=r'[A-Za-z]{3,4}')