from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ollama import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Medical Assistant backend is running"}


@app.get("/ask")
def ask(question: str):
    response = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    return {
        "question": question,
        "answer": response["message"]["content"],
    }