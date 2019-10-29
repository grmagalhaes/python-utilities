"""
##############################################################################################
###                                                                                        ###
### Função para descobrir a bandeira do cartão                                             ###
### Chama o serviço em binlist.net caso ocorra erro, faz validação local                   ###
### Por questões de performance o teste pode ser feito somente localmente                  ###
###                                                                                        ###
### Autor: Gerson Rodrigues                                                                ###
### Organização: N3R                                                                       ###
### Data: 08/07/2019                                                                       ###
###                                                                                        ###
##############################################################################################
"""

import requests


def find_brand_offline(card_num: str):

    card_type = 'Desconhecido'

    amex_2 = ('34', '37')
    master_2 = ('51', '52', '53', '54', '55')
    discover_2 = '65'
    discover_4 = '6011'
    visa_1 = '4'

    # Amex
    if len(card_num) == 15 and card_num[:2] in amex_2:
        card_type = 'Amex'

    # Master, Visa e Discover
    elif len(card_num) == 16:
        # MasterCard
        if card_num[:2] in master_2:
            card_type = 'Master'

        # Discover
        elif (card_num[:2] in discover_2) or (card_num[:4] in discover_4):
            card_type = 'Discover'

        # Visa
        elif card_num[:1] in visa_1:
            card_type = 'Visa'

    # VISA
    elif (len(card_num) == 13) and (card_num[:1] in visa_1):
        card_type = 'Visa'

    return card_type


def find_brand_online(card_num: str):

    binlist_url = "https://lookup.binlist.net/"

    card_num = str(card_num)

    # IIN on the credit card being searched
    card_iin = card_num[:6]

    iin = str(card_iin)

    response = requests.get(binlist_url + iin)

    # Se não retornou sucesso chama a rotina offline
    if response.status_code != 200:
        response = find_brand_offline(card_num)
    else:
        response = response.json()['scheme'].capitalize()
        if response == 'Mastercard':
            response = 'Master'

    return response


def find_brand(card_num: str, mode='online'):
    if mode == 'online':
        return find_brand_online(card_num)
    else:
        return find_brand_offline(card_num)


if __name__ == '__main__':
    """
    '370000000000002': 'Amex'
    '6011000000000012': 'Discover'
    '5424000000000015': 'Master'
    '4007000000027': 'Visa'
    '400700000002' : 'Master' (Desconhecido se offline)
    """
    print("teste online")
    print('6011000000000012: ', find_brand('6011000000000012'))
    print('370000000000002: ', find_brand('370000000000002'))
    print('6011000000000012: ', find_brand('6011000000000012'))
    print('5424000000000015: ', find_brand('5424000000000015'))
    print('4007000000027: ', find_brand('4007000000027'))
    print('400700000002:', find_brand('400700000002'))
    print("teste offline")
    print('6011000000000012: ', find_brand('6011000000000012', 'off'))
    print('370000000000002: ', find_brand('370000000000002', 'off'))
    print('6011000000000012: ', find_brand('6011000000000012', 'off'))
    print('5424000000000015: ', find_brand('5424000000000015', 'off'))
    print('4007000000027: ', find_brand('4007000000027', 'off'))
    print('400700000002:', find_brand('400700000002', 'off'))

    print('400700000002:', find_brand('400700000002', 'off'))
