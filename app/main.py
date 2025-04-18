from builtins import Exception
from fastapi import FastAPI
from starlette.responses import JSONResponse
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.routes import event_routes
from app.utils.api_description import getDescription
import traceback

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    print("[ERROR] Unhandled exception:")
    print(traceback.format_exc())
    return JSONResponse(status_code=500, content={"message": str(exc)})

app.include_router(user_routes.router)
app.include_router(event_routes.router)
