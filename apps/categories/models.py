from pydantic import BaseModel


class Category(BaseModel):
    name: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Electronics",
                "description": "A wide selection of electronic devices, from smartphones and tablets to"
                               " computers and televisions",
            }
        }
