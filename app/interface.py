import time
from datetime import datetime

def titulo(debug=bool):
    print('\n\n\n---------------------------------------------------------')
    print('--------------------DIALED STRESS TEST-------------------')
    print('------------------------Criado por-----------------------')
    print('-------------------------Jjonasxd------------------------')
    print('---------------------------------------------------------\n')

    if not debug:
        time.sleep(3)

def perguntas_obrigatoria():
    print('---------------------------------------------------------')
    print('------------------------Gamemode-------------------------')
    print('---------------------------------------------------------\n')

    print('1. Color.................................................')
    print('2. Color2................................................')
    print('3. Sound.................................................')
    print('4. Time..................................................')
    print('5. Shape.................................................')

    gamemode = input('$: ')

    while gamemode not in ['1', '2', '3', '4', '5']:
        print('\n--------------------Tente Novamente----------------------')
        gamemode = input('$: ')

    print('\n---------------------------------------------------------')
    print('-----------------------Multiplayer-----------------------')
    print('---------------------------------------------------------\n')
    print('1. Lobby.................................................')
    print('2. Challenge...................O Servidor bloqueia rápido')

    multiplayer = input('$: ')

    while multiplayer not in ['1', '2']:
        print('\n--------------------Tente Novamente----------------------')
        multiplayer = input('$: ')

    print('\n-----------------------------------------------------------')
    print('----------------------Requisições--------------------------')
    print('-----------------------------------------------------------\n')
    print('-----------------Quantas requisições por vez---------------\n')

    requisicoes = input('$: ')

    while not requisicoes.isnumeric() or int(requisicoes) <= 0:
        print('\n--------------------Tente Novamente----------------------')
        requisicoes = input('$: ')

    print('-----------------------------------------------------------')
    print('--------------------------Invasão--------------------------')
    print('-----------------------------------------------------------')
    print('-----------Modo que sera utilizado para adivinhar----------\n')
    
    print('1. Casa por Casa...........................................')
    print('2. Aleatorio...............................................')

    adivinhar = input('$: ')

    while adivinhar not in ['1', '2']:
        print('\n--------------------Tente Novamente----------------------')
        adivinhar = input('$: ')

    print('\n-----------------------------------------------------------')
    print('--------------------------Seu Nome-------------------------')
    print('-----------------------------------------------------------')

    nome = input('$: ')

    return {'gamemode': gamemode, 'multiplayer': multiplayer, 'requisicoes': requisicoes, 'adivinhar': adivinhar, 'nome': nome}

def aleatorio_pergunta(perguntas) -> None:
    print('\n-----------------------------------------------------------')
    print('--------------------Quantidade de vezes--------------------')
    print('-----------------------------------------------------------')
    print('---------Quantidade de vezes que o script repetirá---------')
    print('-----------------Permitido números grandes-----------------\n')

    vezes = input('$: ')

    while not vezes.isnumeric() or int(vezes) <= 0:
        print('\n--------------------Tente Novamente----------------------')
        vezes = input('$: ')

    perguntas['vezes'] = vezes

def pronto() -> None:
    print('\n-----------------------------------------------------------')
    print('-----------------------¿Estas Pronto?----------------------')
    print('-----------------------------------------------------------')

    pronto = input('Y/N: ').lower()

    while pronto not in ['y', 'n']:
        print('\n--------------------Tente Novamente----------------------')
        pronto = input('Y/N: ').lower()

    if pronto == 'n':
        raise KeyboardInterrupt('Parabens você cancelou no ultimo minuto >:(')
    
def print_status(status_code, url_api, status_mode, method, tempo, codigo, request_size) -> None:
    status_code_dict = {
        #2xx
        '200': 'OK',
        '201': 'Created',
        '202': 'Accepted',
        #3xx
        "301": "Moved Permanently",
        "302": "Found",
        "304": "Not Modified",
        #4xx
        "400": "Bad Request",
        "401": "Unauthorized",
        "403": "Forbidden",
        "404": "Not Found",
        "405": "Method Not Allowed",
        "408": "Request Timeout",
        "429": "Too Many Requests",
        #5xx
        "500": "Internal Server Error",
        "502": "Bad Gateway",
        "503": "Service Unavailable",
        "504": "Gateway Timeout",
    } # Metade desse dicionario nem vai ser usado kkkkkk

    status_name = status_code_dict.get(str(status_code))

    if not status_name:
        status_name = 'Other'
    if not hasattr(print_status, "numero"):
        print_status.numero = 0
            
    print_status.numero += 1

    if status_mode['presets'] == 'all':
        print(f'\r| {status_code} {status_name} | {url_api} | {method} | {codigo} | {tempo:2f} MS | {request_size} bytes | {datetime.now().isoformat()} | {print_status.numero} |\r')

    elif status_mode['presets'] == 'normal':
        print(f'\r| {status_code} | {url_api} | {method} | {codigo} | {tempo:2f} MS | {request_size} bytes | {print_status.numero} |\r')

    elif status_mode['presets'] == 'lowest':
        print(f'\r| {status_code} {status_name} | {codigo} | {tempo:2f} MS | {print_status.numero} |\r')
    else:
        print(f'\r| {status_code} {status_name} | {url_api} | {method} | {codigo} | {tempo:2f} MS | {request_size} bytes | {print_status.numero} |\r')

def achei(normal_url, code):
    print('\n-----------------------------------------------------------')
    print(f'Acesse: {normal_url}{code}, para jogar com seus novos amigos')
    print('-----------------------------------------------------------')
    