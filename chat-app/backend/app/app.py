from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.exception import register_app_exceptions

from app.routes.auth.route import auth_route


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

app.include_router(auth_route)


register_app_exceptions(app)
