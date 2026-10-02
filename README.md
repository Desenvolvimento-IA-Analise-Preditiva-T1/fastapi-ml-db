# API de Predição de Crédito (Deploy com SQLite)

Este projeto implementa uma API utilizando **FastAPI** para servir predições de Machine Learning, onde o modelo treinado é persistido diretamente em um banco de dados relacional **SQLite** no formato binário (`BLOB`).

---

## Arquitetura do Projeto

1. **Serialização em Binário:** O script `modelo_ml.ipynb` transforma o objeto Python do modelo em uma sequência pura de bytes (`pickle.dumps`).
2. **Persistência Relacional:** O modelo é salvo na tabela `modelos` do banco SQLite (`ia_banco.db`) usando a coluna do tipo `BLOB`.
3. **Leitura no Startup:** A API conecta-se ao banco, faz uma consulta SQL para buscar a versão mais recente do modelo e o desserializa (`pickle.loads`) na memória.
4. **Inferência Segura:** O endpoint `POST /predict` recebe e valida os dados de entrada via **Pydantic** e processa o diagnóstico de crédito.
