from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate, EventUpdate
from typing import List, Optional
from datetime import datetime

class EventService:
    @staticmethod
    async def create_event(db: AsyncSession, event_in: EventCreate) -> Event:
        event = Event(
            title=event_in.title,
            description=event_in.description,
            start_time=event_in.start_time,
            end_time=event_in.end_time,
            capacity=event_in.capacity,
            location=event_in.location
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    @staticmethod
    async def get_event(db: AsyncSession, event_id: int) -> Optional[Event]:
        try:
            query = select(Event).where(Event.id == event_id)
            print(f"[DEBUG] Executing query in get_event: {query}")
            result = await db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"[ERROR] get_event failed: {e}")
            raise

    @staticmethod
    async def list_events(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Event]:
        try:
            query = select(Event).offset(skip).limit(limit)
            print(f"[DEBUG] Executing query in list_events: {query}")
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            print(f"[ERROR] list_events failed: {e}")
            raise

    @staticmethod
    async def update_event(db: AsyncSession, event_id: int, event_in: EventUpdate) -> Optional[Event]:
        event = await EventService.get_event(db, event_id)
        if not event:
            return None
        update_data = event_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)
        await db.commit()
        await db.refresh(event)
        return event

    @staticmethod
    async def delete_event(db: AsyncSession, event_id: int) -> bool:
        event = await EventService.get_event(db, event_id)
        if not event:
            return False
        await db.delete(event)
        await db.commit()
        return True
