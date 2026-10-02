from fastapi import HTTPException
from fastapi import APIRouter

from cliente import DadosCliente

import sqlite3
import pickle


# Função auxiliar para carregar o modelo a partir da tabela (que esta no banco de dados)
def carregar_modelo_da_base_de_dados():
    conexao = sqlite3.connect("ia_banco.db")
    cursor = conexao.cursor()
    
    # Procuramos o registo mais recente do nosso modelo
    cursor.execute("SELECT pesos_binarios FROM modelos WHERE nome_modelo = ? ORDER BY id DESC LIMIT 1", ("modelo_credito",))
    linha = cursor.fetchone()
    conexao.close()
    
    if linha is None:
        raise RuntimeError("Nenhum modelo foi encontrado na base de dados SQLite!")
    
    # Descongelamos os bytes de volta para o objeto do Scikit-Learn
    pesos_binarios = linha[0]
    modelo_carregado = pickle.loads(pesos_binarios)
    return modelo_carregado

# Carregamos o modelo para a memória
modelo = carregar_modelo_da_base_de_dados()


# Criamos o roteador com prefixo
predict_route = APIRouter(prefix="/predict", tags=["Predição"])

# Criamos o endpoint de predição usando POST
@predict_route.post("/predict", tags=["Predição"])
def prever_aprovacao(cliente: DadosCliente):
    """
    Recebe as características do cliente e devolve se o crédito foi Aprovado ou Recusado.
    """
    try:
        # Preparamos os dados no formato de matriz 2D que o modelo espera: [[idade, score]]
        dados_entrada = [[cliente.idade, cliente.pontuacao_credito]]
        
        # Executamos a predição com o modelo congelado
        resultado = modelo.predict(dados_entrada)[0]
        
        # Traduzimos o resultado numérico (0 ou 1) em uma mensagem amigável de negócio
        if resultado == 1:
            status = "Aprovado"
        else:
            status = "Reprovado"
        
        return {
            "idade_informada": cliente.idade,
            "pontuacao_informada": cliente.pontuacao_credito,
            "decisao": status,
            "codigo_decisao": int(resultado)
        }
    except Exception as erro:
        # Tratamento de erros seguro sem derrubar o servidor
        raise HTTPException(status_code=500, detail=f"Erro no processamento da predição: {str(erro)}")