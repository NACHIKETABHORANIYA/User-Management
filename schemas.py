from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class UserManage(BaseModel):
    """
    schema class to manage user functionalities
    """

    company_name: Optional[str] = Field(None, description="name of company")
    password: Optional[str] = Field(None, description="password")
    first_name: Optional[str] = Field(None, description="first name of user")
    email: Optional[str] = Field(None, description="email of user")
    last_name: Optional[str] = Field(None, description="last name of user")
    dob: Optional[str] = Field(None, description="date of birth of user")
    mobile_number: Optional[str] = Field(None, description="mobule number of user")
    hashtag: Optional[str] = Field(None, description="tag of user")


class UserInDB(UserManage):
    id: int

    class Config:
        orm_mode: True


class SendEmailResponse(BaseModel):
    message: str


class SendEmailRequest(BaseModel):
    list_of_users: List[str]
