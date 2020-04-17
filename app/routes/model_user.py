from pydantic import BaseModel, Field

#Request Schema
class UserSchema(BaseModel):
    userName:  str = Field(..., min_length=3, max_length=50, title="username for account settings")
    firstName: str = Field(..., min_length=3, max_length=50, title="First Name of the user")
    lastName:  str = Field(..., min_length=3, max_length=50, title="Last Name of the user")

class UserDB(UserSchema):
    id: int

#Use this schema for the response
# Follow database Name
class UserResponseSchema(BaseModel):
    user_name:  str 
    first_name: str  
    last_name:  str 
    id:         str 
