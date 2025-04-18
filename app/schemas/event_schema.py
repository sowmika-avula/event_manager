from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, example="Annual Tech Conference")
    description: Optional[str] = Field(None, max_length=500, example="A conference for tech enthusiasts.")
    start_time: datetime = Field(..., example="2025-05-01T09:00:00")
    end_time: datetime = Field(..., example="2025-05-01T17:00:00")
    capacity: int = Field(..., ge=1, example=100)
    location: Optional[str] = Field(None, max_length=200, example="Conference Hall A")

    @validator('end_time')
    def end_time_after_start_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, max_length=200)

    @validator('end_time')
    def end_time_after_start_time(cls, v, values):
        if 'start_time' in values and v is not None and values['start_time'] is not None and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class EventResponse(EventBase):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True
