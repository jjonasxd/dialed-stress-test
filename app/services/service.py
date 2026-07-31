from functools import wraps
import secrets
import string
import itertools 
from app.interface import aleatorio_pergunta, pronto, print_status, achei
import asyncio
import time
from datetime import datetime
import os

try:
    import httpx
except ModuleNotFoundError:
    raise SystemExit('\nVocê não instalou a bibilioteca httpx\nPrograma acabou rapaziada >:(')

def traduzir_gamemode(perguntas: dict):
    gamemode = perguntas['gamemode']

    multiplayer = perguntas['multiplayer']
    
    name_gamemodes = ['color', 'color2', 'sound', 'time', 'shape']
    letter_multiplayer = ['l', 'c']

    gindex = int(gamemode) - 1
    url_api_gamemode_name = name_gamemodes[gindex]

    mindex = int(multiplayer) - 1
    url_multiplayer = letter_multiplayer[mindex]

    return url_api_gamemode_name, url_multiplayer

def urls(url_api_gamemode_name, multiplayer, url_multiplayer):
    if multiplayer == '1': # lobby
        url_api = f'https://dialed-api-production.onrender.com/api/{url_api_gamemode_name}/lobby/join'
    else:
        url_api = f'https://dialed-api-production.onrender.com/api/{url_api_gamemode_name}/challenge/'

    if url_api_gamemode_name == 'color':
        url = f'https://dialed.gg/?{url_multiplayer}='
    else:
        url = f'https://dialed.gg/{url_api_gamemode_name}?{url_multiplayer}='

    return {'url_api': url_api, 'url': url}

caracteres = list(string.ascii_uppercase) + list(range(10))

def gerar_codigo_aleatorio():
    Acodigo = []

    for i in range(6):
        Acodigo.append(secrets.choice(caracteres))

    return "".join(map(str, Acodigo))

# Enviar Codigo API
async def enviar_post(client, url, codigo, nome, status_mode, logs):
    if not nome:
        nome = 'HACKER'

    payload = {
        'code': codigo,
        'name': nome
    }

    inicio = time.perf_counter()

    resposta = await client.post(url['url_api'], json=payload) # Isso que envia a requisicao o resto e so de enfeite

    final = time.perf_counter()

    tempo_da_requisicao = (final - inicio) * 1000
    tamanho = len(resposta.content)

    print_status(resposta.status_code, url['url_api'], status_mode, 'POST', tempo_da_requisicao, codigo, tamanho)

    # as condicionais não foi minha ideia
    if logs and (300 <= resposta.status_code < 400 or 500 <= resposta.status_code < 600):
        os.makedirs('app/logs', exist_ok=True)
        with open('app/logs/errors.log', 'a', encoding='utf-8') as arquivo:
            log_content = f"{resposta.status_code} {url['url_api']} {status_mode} GET {tempo_da_requisicao:.2f}ms {codigo} {datetime.now().isoformat()}\n"
            arquivo.write(log_content)
    
    if 200 <= resposta.status_code < 300:
        raise SystemExit(achei(f'{url['url']}', codigo))
        
async def enviar_get(client, url, codigo, status_mode, logs):
    inicio = time.perf_counter()

    url_completa = f"{url['url_api']}{codigo}"
    resposta = await client.get(url_completa)

    final = time.perf_counter()
    tempo_da_requisicao = (final - inicio) * 1000

    print_status(resposta.status_code, url_completa, status_mode, 'GET', tempo_da_requisicao, codigo, 0)

    if logs and (300 <= resposta.status_code < 400 or 500 <= resposta.status_code < 600):
        os.makedirs('app/logs', exist_ok=True)
        with open('app/logs/errors.log', 'a', encoding='utf-8') as arquivo:
            log_content = f"{resposta.status_code} {url_completa} {status_mode} GET {tempo_da_requisicao:.2f}ms {codigo} {datetime.now().isoformat()}\n"
            arquivo.write(log_content)

    if 200 <= resposta.status_code < 300:
        raise SystemExit(achei(f'{url['url']}', codigo))

async def main_requests(codigos, url, nome, status_mode, multiplayer, requisicoes, vezes, timeout, logs):
    async with httpx.AsyncClient(timeout=float(timeout['time'])) as client:
        if codigos:
            if multiplayer == '1':
                tarefas = [enviar_post(client, url, codigo, nome, status_mode, logs) for codigo in codigos]
            else:
                tarefas = [enviar_get(client, url, codigo, status_mode, logs) for codigo in codigos]
        else:
            acode = []
            if multiplayer == '1':
                for i in range(int(vezes)):
                    for i in range(int(requisicoes)):
                        acode.append(gerar_codigo_aleatorio())
                        if len(acode) >= int(requisicoes):
                            tarefas = [enviar_post(client, url, codigo, nome, status_mode, logs) for codigo in acode]
                            acode = []
            else:
               for i in range(int(vezes)):
                    for i in range(int(requisicoes)):
                        acode.append(gerar_codigo_aleatorio())
                        if len(acode) >= int(requisicoes):
                            tarefas = [enviar_get(client, url, codigo, status_mode, logs) for codigo in acode]
                            acode = []
            
        resultado = await asyncio.gather(*tarefas)

def enviar_request_casa(perguntas, urls, status_mode, timeout, logs):
    codigos = []

    for i in itertools.product(caracteres, repeat=6):
        codigo = "".join(map(str, i))
        codigos.append(codigo)

        if len(codigos) >= int(perguntas['requisicoes']):
            res = asyncio.run(main_requests(codigos, urls, perguntas['nome'], status_mode, perguntas['multiplayer'], None, None, timeout, logs))

            if res:
                achei(urls['url'], res)
                break

            codigos = []

def enviar_request_random(perguntas, urls, status_mode, timeout, logs):
    for i in range(int(perguntas['vezes']) + 1):
        asyncio.run(main_requests(None, urls, perguntas['nome'], status_mode, perguntas['multiplayer'], perguntas['requisicoes'], perguntas['vezes'], timeout, logs))

# Função principal que roda as demais
def run_service(app):
    url_api_gamemode_name, url_multiplayer = traduzir_gamemode(app['perguntas'])

    app['urls'] = urls(url_api_gamemode_name, app['perguntas']['multiplayer'], url_multiplayer)

    if app['perguntas']['adivinhar'] == '2':
        aleatorio_pergunta(app['perguntas'])

    pronto()

    if app['perguntas']['adivinhar'] == '1':
        enviar_request_casa(app['perguntas'], app['urls'], app['status_mode'], app['timeout'], app['logs'])
    else:
        enviar_request_random(app['perguntas'], app['urls'], app['status_mode'], app['timeout'], app['logs'])