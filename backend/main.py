from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from compiler.compiler_engine import compile_code


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str
    language: str


@app.get("/")
def home():
    return {
        "message": "AI Smart Compiler Backend Running"
    }


@app.post("/compile")
def compile_program(request: CodeRequest):

    result = compile_code(
        request.code,
        request.language
    )

    return {
        "result": result
    }
