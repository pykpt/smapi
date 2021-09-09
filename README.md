# smapi

[Сайт API](https://api.school.mosreg.ru/)

[Методы API](https://api.school.mosreg.ru/partners/swagger/ui/index)

## Установка
```
pip install https://github.com/pykpt/smapi/archive/main.zip --upgrade
```
## Авторизация
С помощью логина и пароля
```py
from smapi import Client


client = Client(login='login', password='password')
```
С помощью токена
```py
from smapi import Client


client = Client(token='token')
```
## Получение токена
```py
from smapi import Client


client = Client(login='login', password='password')
print(client.token)
```
## Использование
```py
from smapi import Client


client = Client(авторизация)
me = client.get('users/me') # Получение пользователя токена
```