from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/notificar")
async def notiticar(request: Request):
    data = await request.json()
    print("Notificação recebida:", data)
    return {"message": "Notificação recebida com sucesso"}