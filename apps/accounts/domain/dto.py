from pydantic import BaseModel, Field

class RegistrationDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: str = Field(..., max_length=254)
    password: str = Field(..., min_length=8)
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None