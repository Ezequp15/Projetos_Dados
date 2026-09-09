SELECT Categoria, count(Produto) AS 'Quantidade'
FROM vendas
GROUP BY Categoria
ORDER BY 'Quantidade' ASC