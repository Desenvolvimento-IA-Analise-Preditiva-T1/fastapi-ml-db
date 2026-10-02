from fastapi import FastAPI

# Importamos o roteador que criamos no outro arquivo (pessoal cuidado com a sequencia)
from predict_routes import predict_route

# Criamos a aplicação FastAPI
app = FastAPI(
    title="API de Predição de Crédito",
    description="Serviço preditivo para aprovação automática de empréstimos com ML."
)

# Conectamos o roteador de pedidos na aplicação
app.include_router(predict_route)

# uvicorn main:app --reload