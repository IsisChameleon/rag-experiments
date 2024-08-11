import logging
import os

import uvicorn
from application.handlers.oauth_events_handler import log_oauth_event
from containers import AppContainer
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from root.api import auth_router

load_dotenv()
environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

app = FastAPI(debug=(environment == "dev"))

# Set up the DI container
container = AppContainer()
container.wire(modules=[__name__])

# Set up the event bus and register event handlers
event_bus = container.event_bus()
event_bus().subscribe("UserOAuthCompleted", log_oauth_event)

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Redirect to documentation page when accessing base URL
    @app.get("/")
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")


def mount_static_files(directory, path):
    if os.path.exists(directory):
        app.mount(path, StaticFiles(directory=directory), name=f"{directory}-static")


# Mount the data files to serve the file viewer
mount_static_files("data", "/api/files/data")
# Mount the output files from tools
mount_static_files("tool-output", "/api/files/tool-output")

app.include_router(auth_router, prefix="/oauth")


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))
    reload = True if environment == "dev" else False

    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)
