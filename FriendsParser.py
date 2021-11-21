import requests
import csv
import json
import codecs


class FriendsParser():
    def __init__(self, access_token, user_ids,
                 output_format='csv', output_path='report'):

        self.access_token = str(access_token)
        self.user_ids = str(user_ids)
        self.output_path = str(output_path)
        self.output_format = str(output_format)

        self.__version = 5.131
        self.__required_user_id = FriendsParser.__get_id(self)
        self.__data = FriendsParser.__get_data(self,
                                               self.__required_user_id)

    #   Преобразование в ISO
    def __time_handle(self, time):
        time = time.split('.')
        if len(time) == 3:
            time.reverse()
            return '-'.join(time)
        else:
            time.append('YYYY')
            time.reverse()
            return '-'.join(time)

    def __get_id(self):
        response = requests.get('https://api.vk.com/method/users.get', params={
                                        'access_token': self.access_token,
                                        'user_ids': self.user_ids,
                                        'name_case': 'nom',
                                        'v': self.__version
                                    })

        user_data = response.json()
        return user_data['response'][0]['id']

    def __get_data(self, user_id):
        fields = 'sex, bdate, city, country'
        response = requests.get('https://api.vk.com/method/friends.get',
                                params={
                                        'access_token': self.access_token,
                                        'user_id': user_id,
                                        'fields': fields,
                                        'order': 'name',
                                        'name_case': 'nom',
                                        'v': self.__version
                                    })

        data = response.json()
        user_list = []
        for i in data['response']['items']:

            user = {'name': i['first_name'],
                    'last_name': i['last_name']}

            if 'country' in i:
                user['country'] = i['country']['title']

            else:
                user['country'] = 'unknown'

            if 'city' in i:
                user['city'] = i['city']['title']

            else:
                user['city'] = 'unknown'

            if 'bdate' in i:
                user['bdate'] = FriendsParser.__time_handle(self, i['bdate'])

            else:
                user['bdate'] = 'unknown'

            if 'sex' in i:
                if i['sex'] == 1:
                    user['sex'] = 'ж'
                else:
                    user['sex'] = 'м'

            else:
                user['sex'] = 'unknown'

            user_list.append(user)

        return user_list

    def __get_csv(self, data):
        FILENAME = ''
        if self.output_path[-4:] == '.csv':
            FILENAME = self.output_path
        else:
            FILENAME = self.output_path + '.csv'

        with open(FILENAME, "w", newline="", encoding='utf-8') as file:
            columns = ["name", "last_name", "country", "city", "bdate", "sex"]
            writer = csv.DictWriter(file, fieldnames=columns, )
            writer.writeheader()
            writer.writerows(data)

    def __get_json(self, data):
        FILENAME = ''
        if self.output_path[-4:] == '.json':
            FILENAME = self.output_path
        else:
            FILENAME = self.output_path + '.json'

        with open(FILENAME, 'wb') as f:
            json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)

    def __get_tsv(self, data):
        FILENAME = ''
        if self.output_path[-4:] == '.tsv':
            FILENAME = self.output_path
        else:
            FILENAME = self.output_path + '.tsv'

        with open(FILENAME, 'w', encoding='utf-8') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            for record in data:
                writer.writerow([record['name'], record['last_name'],
                                 record['country'], record['city'],
                                 record['bdate'], record['sex']])

    def get_list(self):
        if self.output_format == 'csv':
            FriendsParser.__get_csv(self, self.__data)

        if self.output_format == 'json':
            FriendsParser.__get_json(self, self.__data)

        if self.output_format == 'tsv':
            FriendsParser.__get_tsv(self, self.__data)
