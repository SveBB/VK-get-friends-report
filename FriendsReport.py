from FriendsParser import FriendsParser
import os


def CheckInquiry(inquiry):
    inquiry_params = {'access_token': '',
                      'user_ids': '',
                      'format': 'csv',
                      'path': 'report.csv'}

    inquiry = inquiry.split(' ')

    #   Проверка ключевого слвоа
    if inquiry[0] != 'get':
        raise Exception("ERROR: BAD COMMAND")

    #   Проверка токена
    try:
        inquiry_params['access_token'] = inquiry[1]
    except IndexError:
        raise Exception("ERROR: BAD ACCES_TOKEN")

    #   Првоерка id
    try:
        inquiry_params['user_ids'] = inquiry[2]
    except IndexError:
        raise Exception()("ERROR: BAD USER_IDS")

    # Проверка параметров
    format_list = ['csv', 'tsv', 'json']
    if '-f' in inquiry:
        index = inquiry.index('-f')+1
        FORMAT = inquiry[index]
        if FORMAT in format_list:
            inquiry_params['format'] = FORMAT
        else:
            raise Exception('ERROR: BAD FORMAT')

    if '-p' in inquiry:
        index = inquiry.index('-p')+1
        PATH = inquiry[index]
        try:
            with open(PATH, "w", newline="", encoding='utf-8'):
                inquiry_params['path'] = PATH
            os.remove(PATH)
        except FileNotFoundError:
            raise Exception("ERROR: BAD PATH")

    return inquiry_params


if __name__ == "__main__":
    inquiry = input(':::')
    params = CheckInquiry(inquiry)
    try:
        parser = FriendsParser(params['access_token'], params['user_ids'],
                               params['format'], params['path'])
    except KeyError:
        raise Exception('ERROR: BAD ACCESS_TOKEN OR USER_IDS')

    parser.get_list()

    print('Successfully!')
