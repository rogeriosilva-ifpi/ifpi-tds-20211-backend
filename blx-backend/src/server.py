from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.routers import rotas_produtos, rotas_auth, rotas_pedidos
from src.jobs.write_notification import write_notification

app = FastAPI()
# uvicorn src.server:app --reload --reload-dir=src

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

# Rotas SEGURANÇA: Autenticação e Autorização
app.include_router(rotas_auth.router, prefix="/auth")

# Rotas PEDIDOS
app.include_router(rotas_pedidos.router)


@app.post('/send_email/{email}')
def send_email(email: str, background: BackgroundTasks):
    background.add_task(write_notification,
                        email, 'Olá tudo bem?!')
    return {'OK': 'Mensagem enviada'}

# Middlewares


@app.middleware('http')
async def tempoMiddleware(request: Request, next):
    print('Interceptou Chegada...')

    response = await next(request)

    print('Interceptou Volta ...')

    return response
