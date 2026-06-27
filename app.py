from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router

app = FastAPI(
    title="Portfolio Chatbot",
    version="2.0"
)

# Allow React frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your React app's URL (e.g., ["http://localhost:3000"]) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Portfolio Chatbot API"
    }