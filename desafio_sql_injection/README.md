# Desafio sql injection DVWA

## O desafio:

Entrar no website e encontrar a ganhar acesso aos bancos de dados, através dos inputs de formulário

## Passo a passo:

O passo a passo está no [arquivo](desafio_professor). Este passo a passo foi a forma que consegui encontrar os resultados, executando diretamente no console do navegador :)

## Plus:

Durante conversa com o professor, levantamos a possibilidade da escrita de um script sem necessidade de interface front web que iria direto no servidor e buscasse os itens. Pensando nisto, desenvolvi um pequeno [código](solution/sql_inject.py) utilizando requests e bs4 para chegar lá :)