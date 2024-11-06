from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class SubscriberData(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    gender: Optional[str] = None
    last_updated_timestamp: datetime
    date_of_birth: Optional[datetime] = None
    subscription_active: bool
    roles: List[str] = Field(default_factory=list)
    acl: dict = Field(default_factory=dict)
