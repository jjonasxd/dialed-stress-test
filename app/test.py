def criador_de_prints():
    p = '---------------------------------------------------------'
    len_p = 57
    texto = 'Oi'
    len_texto = len(texto)
    hifens = round(len_p / 2, 0)

    print(f'\n\n{'-' * int(hifens)}{texto}{'-' * int(hifens)}')


def debugs():
    criador_de_prints()