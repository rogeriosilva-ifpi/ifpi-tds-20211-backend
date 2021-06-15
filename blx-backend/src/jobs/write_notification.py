def write_notification(email: str, mensagem=''):
    with open('log.txt', mode='a') as email_file:
        conteudo = f'Email: {email} - msg: {mensagem}\n'
        email_file.write(conteudo)
