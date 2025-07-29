from fastapi import FastAPI

app= FastAPI()



@app.get('/')
def get_products():
    return {"Rodando!": "FastAPI!"}

products = get_products()