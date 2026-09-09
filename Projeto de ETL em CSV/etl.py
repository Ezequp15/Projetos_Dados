import os
import glob
import pandas as pd
from sqlalchemy import create_engine

PASTA_DADOS = "data"
BANCO_DADOS = "vendas.db"
NOME_TABELA = "vendas"

def extrair_dados(pasta: str = PASTA_DADOS) -> pd.DataFrame:

    caminho_busca = os.path.join(pasta, "vendas_*.csv")
    arquivos_csv = sorted(glob.glob(caminho_busca))

    if not arquivos_csv:
        raise FileNotFoundError(
            f"Nenhum arquivo 'vendas_*.csv' encontrado em '{pasta}/'. "
            "Rode 'python gerar_dados_exemplo.py' primeiro, ou coloque seus "
            "próprios CSVs nessa pasta."
        )

    print(f"[EXTRACT] {len(arquivos_csv)} arquivo(s) encontrado(s):")

    dataframes = []
    for arquivo in arquivos_csv:
        df_temp = pd.read_csv(arquivo)
        df_temp["arquivo_origem"] = os.path.basename(arquivo)
        dataframes.append(df_temp)
        print(f"  - {os.path.basename(arquivo)}: {len(df_temp)} linhas")

    df_bruto = pd.concat(dataframes, ignore_index=True)
    print(f"[EXTRACT] Total consolidado: {len(df_bruto)} linhas\n")
    return df_bruto

def _limpar_preco(valor) -> float | None:

    if pd.isnull(valor):
        return None
    texto = str(valor).strip().replace("R$", "").strip()
    texto = texto.replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    print("[TRANSFORM] Nulos por coluna (antes da limpeza):")
    print(df.isnull().sum().to_string())
    print()

    linhas_antes = len(df)
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Duplicatas exatas removidas: {linhas_antes - len(df)}")

    df["Categoria"] = df["Categoria"].astype(str).str.strip().str.upper()

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Preco_Unitario"] = df["Preco_Unitario"].apply(_limpar_preco)
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")

    linhas_antes = len(df)
    df = df.dropna(subset=["Quantidade", "Data"])
    print(f"[TRANSFORM] Linhas removidas por Quantidade/Data ausente: "
          f"{linhas_antes - len(df)}")

    df["Preco_Unitario"] = df.groupby("Categoria")["Preco_Unitario"].transform(
        lambda serie: serie.fillna(serie.median())
    )

    df["Preco_Unitario"] = df["Preco_Unitario"].fillna(df["Preco_Unitario"].median())

    df["Quantidade"] = df["Quantidade"].astype(int)

    df["Receita_Total"] = df["Quantidade"] * df["Preco_Unitario"]
    df["Ano"] = df["Data"].dt.year
    df["Mes"] = df["Data"].dt.month

    print("\n[TRANSFORM] Nulos por coluna (depois da limpeza):")
    print(df.isnull().sum().to_string())
    print(f"\n[TRANSFORM] Total de linhas após transformação: {len(df)}\n")

    return df

def carregar_dados(df: pd.DataFrame, banco: str = BANCO_DADOS, tabela: str = NOME_TABELA):

    engine = create_engine(f"sqlite:///{banco}")
    df.to_sql(tabela, con=engine, if_exists="replace", index=False)

    with engine.connect() as conexao:
        resultado = pd.read_sql(f"SELECT COUNT(*) AS total FROM {tabela}", conexao)

    print(f"[LOAD] {len(df)} linhas gravadas na tabela '{tabela}' de '{banco}'")
    print(f"[LOAD] Verificação pós-carga: {resultado['total'][0]} linhas na tabela\n")

    return engine

def gerar_grafico_receita_por_categoria(engine, caminho_saida="assets/receita_por_categoria.png"):
    import matplotlib.pyplot as plt

    consulta = """
        SELECT Categoria, SUM(Receita_Total) AS receita
        FROM vendas
        GROUP BY Categoria
        ORDER BY receita DESC
    """
    df_receita = pd.read_sql(consulta, engine)

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(df_receita["Categoria"], df_receita["receita"], color="#4C72B0")
    ax.set_title("Receita total por categoria (Jan-Mar/2024)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Receita (R$)")
    ax.bar_label(barras, fmt="R$ %.0f", padding=3, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150)
    plt.close(fig)

    print(f"[BONUS] Gráfico salvo em '{caminho_saida}'\n")

def main():
    df_bruto = extrair_dados()
    df_limpo = transformar_dados(df_bruto)
    engine = carregar_dados(df_limpo)
    gerar_grafico_receita_por_categoria(engine)

    print("Pipeline ETL concluído com sucesso.")
    print(f"Consulte os dados com: SELECT * FROM {NOME_TABELA} LIMIT 10;  "
          f"(em '{BANCO_DADOS}')")


if __name__ == "__main__":
    main()
