from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, oauth2
from src.schemas.schemas import Usuario, UsuarioSimples

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def decodificar_token(token):
    return UsuarioSimples(nome='Rogério', telefone='(86) 99459-3247')


def obter_usuario_logado(token: str = Depends(oauth2_schema)):
    usuario = decodificar_token(token)
    return usuario


@router.get('/me')
def meus_dados(usuario_logado: Usuario = Depends(obter_usuario_logado)):
    return usuario_logado
