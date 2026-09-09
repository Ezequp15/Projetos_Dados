import random
import pandas as pd

random.seed(42)

CATEGORIAS = ["Eletrônicos", "Móveis", "Papelaria", "Vestuário", "Alimentos"]
PRODUTOS = {
    "Eletrônicos": ["Fone de Ouvido", "Mouse", "Teclado", "Carregador", "Caixa de Som"],
    "Móveis": ["Cadeira", "Mesa", "Estante", "Luminária"],
    "Papelaria": ["Caderno", "Caneta", "Agenda", "Pasta"],
    "Vestuário": ["Camiseta", "Boné", "Jaqueta"],
    "Alimentos": ["Café", "Barra de Cereal", "Água Mineral"],
}
REGIOES = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
CLIENTES = [f"Cliente {i:03d}" for i in range(1, 31)]

PRECO_BASE = {
    "Eletrônicos": (35.0, 250.0),
    "Móveis": (120.0, 600.0),
    "Papelaria": (2.0, 25.0),
    "Vestuário": (25.0, 120.0),
    "Alimentos": (3.0, 18.0),
}

def _variacao_categoria(categoria: str) -> str:
    formatos = [
        categoria.upper(),
        categoria.lower(),
        f" {categoria} ",
        categoria,
        categoria.upper() + " ",
    ]
    return random.choice(formatos)


def _variacao_preco(preco: float) -> str:

    estilo = random.choice(["ponto", "virgula", "espacos", "moeda"])
    if estilo == "ponto":
        return f"{preco:.2f}"
    if estilo == "virgula":
        return f"{preco:.2f}".replace(".", ",")
    if estilo == "espacos":
        return f" {preco:.2f} "
    return f"R$ {preco:.2f}".replace(".", ",")


def gerar_mes(ano: int, mes: int, n_linhas: int, id_inicial: int) -> pd.DataFrame:
    linhas = []
    ultimo_dia = 28 if mes == 2 else 30
    for i in range(n_linhas):
        categoria_real = random.choice(CATEGORIAS)
        produto = random.choice(PRODUTOS[categoria_real])
        dia = random.randint(1, ultimo_dia)
        preco_min, preco_max = PRECO_BASE[categoria_real]
        preco = round(random.uniform(preco_min, preco_max), 2)

        linhas.append(
            {
                "ID_Pedido": id_inicial + i,
                "Data": f"{ano}-{mes:02d}-{dia:02d}",
                "Cliente": random.choice(CLIENTES),
                "Categoria": _variacao_categoria(categoria_real),
                "Produto": produto,
                "Quantidade": random.randint(1, 8),
                "Preco_Unitario": _variacao_preco(preco),
                "Regiao": random.choice(REGIOES),
            }
        )

    df = pd.DataFrame(linhas)

    idx_nulos_qtd = random.sample(range(len(df)), k=max(1, len(df) // 12))
    df.loc[idx_nulos_qtd, "Quantidade"] = None

    idx_nulos_preco = random.sample(range(len(df)), k=max(1, len(df) // 10))
    df.loc[idx_nulos_preco, "Preco_Unitario"] = None

    return df


def main():
    df_jan = gerar_mes(2024, 1, n_linhas=20, id_inicial=1000)
    df_fev = gerar_mes(2024, 2, n_linhas=18, id_inicial=2000)
    df_mar = gerar_mes(2024, 3, n_linhas=15, id_inicial=3000)

    df_jan = pd.concat([df_jan, df_jan.iloc[[2, 7]]], ignore_index=True)
    df_fev = pd.concat([df_fev, df_fev.iloc[[4]]], ignore_index=True)

    df_jan.to_csv("data/vendas_jan.csv", index=False)
    df_fev.to_csv("data/vendas_fev.csv", index=False)
    df_mar.to_csv("data/vendas_mar.csv", index=False)

    print("Arquivos gerados em data/:")
    print(f"  vendas_jan.csv -> {len(df_jan)} linhas")
    print(f"  vendas_fev.csv -> {len(df_fev)} linhas")
    print(f"  vendas_mar.csv -> {len(df_mar)} linhas")


if __name__ == "__main__":
    main()
