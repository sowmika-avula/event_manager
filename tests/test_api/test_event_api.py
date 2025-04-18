import pytest
from httpx import AsyncClient
from app.main import app
from app.schemas.event_schema import EventCreate
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_and_get_event(async_client):
    event_data = {
        "title": "Test Event",
        "description": "A test event.",
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "capacity": 50,
        "location": "Test Hall"
    }
    response = await async_client.post("/events/", json=event_data)
    if response.status_code != 201:
        print("RESPONSE CONTENT:", response.text)
    assert response.status_code == 201
    event = response.json()
    assert event["title"] == event_data["title"]
    # Get event by ID
    get_response = await async_client.get(f"/events/{event['id']}")
    if get_response.status_code != 200:
        print("RESPONSE CONTENT:", get_response.text)
    assert get_response.status_code == 200
    get_event = get_response.json()
    assert get_event["title"] == event_data["title"]

@pytest.mark.asyncio
async def test_list_events(async_client):
    response = await async_client.get("/events/")
    if response.status_code != 200:
        print("RESPONSE CONTENT:", response.text)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_and_delete_event(async_client):
    # Create an event first
    event_data = {
        "title": "Update Event",
        "description": "To be updated.",
        "start_time": (datetime.now() + timedelta(days=2)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=2, hours=1)).isoformat(),
        "capacity": 30,
        "location": "Room 1"
    }
    create_response = await async_client.post("/events/", json=event_data)
    if create_response.status_code != 201:
        print("RESPONSE CONTENT:", create_response.text)
    assert create_response.status_code == 201
    event = create_response.json()
    event_id = event["id"]
    # Update
    update_data = {"title": "Updated Title"}
    update_response = await async_client.put(f"/events/{event_id}", json=update_data)
    if update_response.status_code != 200:
        print("RESPONSE CONTENT:", update_response.text)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"
    # Delete
    delete_response = await async_client.delete(f"/events/{event_id}")
    if delete_response.status_code != 204:
        print("RESPONSE CONTENT:", delete_response.text)
    assert delete_response.status_code == 204
    # Confirm deletion
    get_response = await async_client.get(f"/events/{event_id}")
    if get_response.status_code != 404:
        print("RESPONSE CONTENT:", get_response.text)
    assert get_response.status_code == 404
