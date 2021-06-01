from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


def verificar_hash(texto_plano, texto_hashed):
    return pwd_context.verify(texto_plano, texto_hashed)


def gerar_hash(texto_plano):
    return pwd_context.hash(texto_plano)
