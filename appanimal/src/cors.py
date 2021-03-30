from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def cors(app: FastAPI):

    origins = [
        'http://localhost:5500'
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
