# 📊 Projeto de ETL em arquivos CSV

Automação em **ETL (Extract, Transform, Load)** que consolida relatórios mensais de vendas em CSV e carrega o resultado em um banco de dados **SQLite** via `SQLAlchemy`.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-CC2927)

## 🎯 Objetivo do projeto

Simular um cenário comum no dia a dia de dados onde uma empresa recebe **relatórios de vendas mensais em CSV**, contendo pequenas inconsistências e precisa automatizar o processo de:

1. **Extract** — ler e unificar todos os arquivos de uma pasta;
2. **Transform** — limpa, e padroniza os dados;
3. **Load** — coloca o resultado em um banco de dados relacional.

## 🛠️ Tecnologias Utilizadas

- [pandas](https://pandas.pydata.org/) — leitura, limpeza e transformação dos dados
- [SQLAlchemy](https://www.sqlalchemy.org/) — conexão e carga no banco SQLite
- [Matplotlib](https://matplotlib.org/) — visualização de apoio
