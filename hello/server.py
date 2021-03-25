from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4


app = FastAPI()

# Objeto Produto


class Produto(BaseModel):
    id: Optional[str]
    nome: str
    preco: float


# Lista de Produtos (funcionará como BD)
bd_produtos: List[Produto] = []


@app.post('/produtos')
def cadastrar_produto(produto: Produto):
    produto.id = str(uuid4())
    bd_produtos.append(produto)
    return produto


@app.get('/produtos')
def listar_produtos():
    return bd_produtos


@app.delete('/produtos/{id}')
def remover_produtos(id: str):
    # procurar produto pelo id
    indice_produto = -1
    for indice, produto in enumerate(bd_produtos):
        print(produto.id, id)
        if produto.id == id:
            indice_produto = indice
            break

    # usar pop para remover o produto
    if indice_produto != -1:
        bd_produtos.pop(indice_produto)
        return {'mensagem': f'Produto {produto.nome} removido com sucesso!'}
    else:
        return {'erro': f'Não foi localizado o produto com id {id}'}


@app.get('/saudacao/{nome}')
def saudacao(nome: str):
    texto = f'Olá {nome}, tudo em paz?!'
    return {"mensagem": texto}


@app.get('/quadrado/{numero}')
def quadrado(numero: int):
    resultado = numero * numero
    texto = f'O quadrado de {numero} é {resultado}'

    return {"mensagem": texto}


@app.get('/dobro')
def dobro(valor: int):
    resultado = 2 * valor
    return {"resultado": f'O dobro de {valor} é {resultado}'}


@app.get('/area-retangulo')  # ?nome=valor
def area_retangulo(largura: int, altura: int = 2):
    area = largura * altura
    return {'area': area}
