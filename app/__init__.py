from app.interface import *
from app.test import debugs

from app.services.service import run_service

try:
    import httpx
except ModuleNotFoundError:
    raise SystemExit('\nVocê não instalou a bibilioteca httpx\nPrograma acabou rapaziada >:(')

def create_app(debug: bool):
    """Factory: Responsável por criar o app"""

    app_context = {
        'debug': debug,
        'app_name': 'Dialed Stress Test',
        'version': '1.0.0',
        'perguntas': None,
        'urls': {},
        'status_mode': { # Personalize isso, é o que você vê durante o processo
            'presets': 'normal', # normal, lowest, all (para nerds), dica caso queria personalizar mais acesse app/interface.py e procure pela funcao print_status
        },
        'logs': True,
        'status_protection': True, # em desenvolvimento, Cancela o programa se tiver muitos 429 ou 5xx errors
        'timeout': {
            'time': '10' # em segundos
        }
    }

    return app_context

def run_app(app):
    """Run application: Reponsavel por organizar os serviços"""
    try:
        titulo(app['debug'])
        app['perguntas'] = perguntas_obrigatoria()

        run_service(app)

        if app['debug']:
            print('Rodando o modo Debug')
            debugs()
    except KeyboardInterrupt, SystemExit:
        raise SystemExit('\n\nPrograma acabou rapaziada >:(')
    except httpx.PoolTimeout:
        raise SystemExit('\nO tempo de requisição foi escotado se quiser mais vá ao __init__.py\nPrograma acabou rapaziada >:(')
    except httpx.ConnectError:
        raise SystemExit('\nNão foi possivel se conectar com o servidor\nPrograma acabou rapaziada >:(')
