from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import rotas_produtos, rotas_usuarios, rotas_pedidos, rotas_auth

app = FastAPI()

# CORS
origins = ['http://localhost:3000',
           'https://myapp.vercel.com']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

# Rotas PRODUTOS
app.include_router(rotas_produtos.router)

# Rotas USUARIOS
app.include_router(rotas_usuarios.router)

# Rotas PEDIDOS
app.include_router(rotas_pedidos.router)

# Rotas Autenticação
app.include_router(rotas_auth.router, prefix='/auth')
