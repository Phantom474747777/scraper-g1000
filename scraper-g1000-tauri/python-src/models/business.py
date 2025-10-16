from pydantic import BaseModel, Field
from typing import Optional

class BusinessData(BaseModel):
    name: str = Field(..., description="The name of the business or entity.")
    address: str = Field(..., description="The address of the business or entity.")
    phone_number: str = Field(..., description="The phone number of the business or entity.")
    website: str = Field(..., description="The website URL of the business or entity.")
    email: Optional[str] = Field(default="N/A", description="The email address of the business or entity if available.")