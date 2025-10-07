from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def read_root():
    return {"Hello":"Wdorld"}
@app.get("/hello/{name}")
def greet_name(name:str):
    return {"greeting":f"Hello, {name}!"}


