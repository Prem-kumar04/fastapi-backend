from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):

    username: str

    email: EmailStr

    first_name: str

    last_name: str

    password: str

    role_id: int


class LoginRequest(BaseModel):

    email: EmailStr

    password: str
