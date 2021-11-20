VK get friends report - консольное приложение для получения списка друзей пользователя ВК
Для получение списка воспользуйтесь командой get

Пример запроса: get ACCESS_TOKEN USER_IDS -f FILE_FORMAT -p FILE_PATH

    ACCESS_TOKEN - ваш токен доступа (Обязательный параметр)
    USER_IDS - id пользвателя для которого нужно составить список (Обязательный параметр)
    FILE_FORMAT - формат файла (Необязательный параметр, по умолчанию - CSV)
    FILE_PATH - путь сохранения файла (Необязательный параметр, по умолчанию - файл с именем report в текущей директории)

get 77bd4696e600760cdc70d676967acd457aee301ccee708a64e680d9e223ac94061b32b168baec4c931c9c nataxamy -p C:/Users/SveBB/Desktop/test -f json

https://oauth.vk.com/authorize?client_id=8005691&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,friends&response_type=token&v=5.131