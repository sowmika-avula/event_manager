from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse
from app.services.event_service import EventService
from app.dependencies import get_db

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event_in: EventCreate, db: AsyncSession = Depends(get_db)):
    event = await EventService.create_event(db, event_in)
    return event

@router.get("/", response_model=List[EventResponse])
async def list_events(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    return await EventService.list_events(db, skip=skip, limit=limit)

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await EventService.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, event_in: EventUpdate, db: AsyncSession = Depends(get_db)):
    event = await EventService.update_event(db, event_id, event_in)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await EventService.delete_event(db, event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return None
