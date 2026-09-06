from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def iniciar():
    return {"estado": "api activa"}
