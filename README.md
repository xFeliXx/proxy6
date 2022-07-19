# [Proxy6.net](https://proxy6.net) API
Библиотека для работы с API сайта [Proxy6.net](https://proxy6.net)  
Их документация доступна по [ссылке](https://proxy6.net/developers).
Есть синхронный и асинхронный клиент.

### Установка
Напрямую с помощью pip и git:
```sh
pip install git+https://github.com/LulzLoL231/pyProxy6
```
Или из исходников:
```sh
git clone https://github.com/LulzLoL231/pyProxy6
cd pyProxy6
python3 setup.py install
```

### Пример получения баланса
Вообще API не предусматривает отдельное получение информации о балансе, но он возвращает эту информацую в каждом ответе.
```python
from asyncio import run

from proxy6 import Proxy6
from proxy6 import AsyncProxy6


proxy6 = Proxy6('%API_KEY%')
count = proxy6.get_country()  # Получаем информацию о доступных локациях для прокси.


async def get_proxies():
    async_proxy6 = AsyncProxy6('%API_KEY%')
    proxies = await async_proxy6.get_proxy()  # Получаем информацию обо всех купленных прокси.
    return list(proxies.list.values())  # Возвращаем список купленных прокси.


proxies = run(get_proxies())
print(f'Ваш баланс: {count.balance} {count.currency}')
print(f'У вас куплено {len(proxies)} прокси.')
```
