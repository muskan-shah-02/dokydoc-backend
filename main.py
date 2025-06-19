from fastapi import FastAPI
from app.api.endpoints import login

# Create the main FastAPI application instance
app = FastAPI(title="Doky Project API")

# Include the router from the login endpoints module.
# All routes defined in login.router will now be part of our app.
app.include_router(login.router, tags=["Users"])


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Doky Project API!"}

