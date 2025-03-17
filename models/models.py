from pydantic import BaseModel
from typing import Dict, Any,List
from fastapi import File, Form, UploadFile



class User(BaseModel):
    fullname: str
    email: str
    typeo: str
    password: str
    
    class Config:
        from_attributes = True  

class Userlogin(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True  

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True  


class TokenData(BaseModel):
    username: str | None = None

    class Config:
        from_attributes = True  



class ImageModel(BaseModel):
    username: str
    filename: str  
    content_type: str  
    image_link: str 
    event_name : str
    event_date : str 
    embeddings : Dict[str, Any] 

    class Config:
       from_attributes = True  



class ImageUploadResponse(BaseModel):
    username: str
    event_name: str 
    event_date: str 
    images: List[UploadFile] 
    class Config:
       from_attributes = True  

class Message(BaseModel):
    message: str
    username: str
    class Config:
       from_attributes = True  
