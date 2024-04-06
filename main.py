from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define a list of origins that should be permitted to make cross-origin requests
origins = [
    "http://localhost:3000",  # React app's origin in development
    "http://localhost:8080",  # React app's origin in development
    "https://your-react-app-production-domain.com",  # React app's production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/api/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
