from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, boards, tasks, time_tracking, reports

app = FastAPI(
    title="Time Tracking App",
    description="Ứng dụng theo dõi thời gian làm việc trên các task",
    version="1.0.0"
)

# CORS configuration
origins = [
    "*",  # Trong production nên giới hạn domain cụ thể
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(boards.router)
app.include_router(tasks.router)
app.include_router(time_tracking.router)
app.include_router(reports.router)

# Root endpoint
@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to the Time Tracking App"}
