from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.core import Base, engine
from .routes.login import router as login_route
from .routes.signup import router as signup_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login_route)
app.include_router(signup_router)
