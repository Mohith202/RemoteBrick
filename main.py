from fastapi import FastAPI
from routes.user import router as user_router

# FastAPI instance
app = FastAPI()

# Include the user router
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
