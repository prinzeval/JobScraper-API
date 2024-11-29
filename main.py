from fastapi import FastAPI

app = FastAPI()

@app.post("/")
def home():
    return "helloworld"
