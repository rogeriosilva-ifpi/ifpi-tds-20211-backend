
from pydantic import BaseModel
from typing import Optional, List


class Usuario(BaseModel):
    id: Optional[str] = None
    nome: str
    telefone: str
    # produtos: List[produtos] = []


class Produto(BaseModel):
    id: Optional[str] = None
    nome: str
    detalhes: str
    preco: float
    disponivel: bool = False

    class Config:
        orm_mode = True


class ProdutoSimples(BaseModel):
    id: Optional[str] = None
    nome: str
    preco: float

    class Config:
        orm_mode = True


class Pedido(BaseModel):
    id: Optional[str] = None
    quantidade: int
    entrega: bool = True
    endereco: str
    observacoes: Optional[str] = 'Sem observações'
