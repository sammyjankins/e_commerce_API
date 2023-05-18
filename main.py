from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.user.routers import router as user_router
from apps.categories.routers import router as cat_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=["Users"], prefix="/user")
app.include_router(cat_router, tags=["Categories"], prefix="/category")
