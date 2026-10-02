from pydantic import BaseModel

# Criamos o "Schema" com Pydantic (O segurança da porta)
# Ele define exatamente quais campos o cliente É OBRIGADO a enviar e os seus tipos
class DadosCliente(BaseModel):
    idade: int
    pontuacao_credito: int
