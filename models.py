from pydantic import BaseModel

class Patient(BaseModel):
     first_name: str
     last_name: str
     address: str
     age: int