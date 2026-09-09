# 📊 Projeto de ETL em arquivos CSV

## 🎯 Objetivo do projeto

Simular um cenário comum no dia a dia de dados: uma empresa recebe **relatórios de vendas mensais em CSV**, exportados por sistemas diferentes (ou por pessoas diferentes), cheios de pequenas inconsistências — nulos, duplicatas, texto com espaços/caixa variando, preços em formatos diferentes. Este projeto automatiza:

1. **Extract** — ler e unificar todos os arquivos de uma pasta;
2. **Transform** — limpar, padronizar e enriquecer os dados;
3. **Load** — persistir o resultado em um banco de dados relacional.

## ▶️ Como rodar o projeto

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/etl-vendas-pandas.git
cd etl-vendas-pandas

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. (Opcional) gere novos dados de exemplo — o repositório já vem com os CSVs prontos
python gerar_dados_exemplo.py

# 5. Rode o pipeline
python etl.py
```

Ao final, você terá:
- `vendas.db` — banco SQLite com a tabela `vendas` já limpa e enriquecida;
- `assets/receita_por_categoria.png` — gráfico de receita por categoria.

### Exemplo de saída no terminal

```
[EXTRACT] 3 arquivo(s) encontrado(s):
  - vendas_fev.csv: 19 linhas
  - vendas_jan.csv: 22 linhas
  - vendas_mar.csv: 15 linhas
[EXTRACT] Total consolidado: 56 linhas

[TRANSFORM] Duplicatas exatas removidas: 3
[TRANSFORM] Linhas removidas por Quantidade/Data ausente: 3
[TRANSFORM] Total de linhas após transformação: 50

[LOAD] 50 linhas gravadas na tabela 'vendas' de 'vendas.db'
[LOAD] Verificação pós-carga: 50 linhas na tabela

Pipeline ETL concluído com sucesso.
```

## 🛠️ Tecnologias Utilizadas

- [pandas](https://pandas.pydata.org/) — leitura, limpeza e transformação dos dados
- [SQLAlchemy](https://www.sqlalchemy.org/) — conexão e carga no banco SQLite
- [Matplotlib](https://matplotlib.org/) — visualização de apoio
