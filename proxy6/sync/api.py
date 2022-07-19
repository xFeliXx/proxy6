# -*- coding: utf-8 -*-
#
#  pyProxy6 API: API.
#  Created by LulzLoL231 at 02/07/22
#
import logging
from time import sleep
from urllib.parse import urlencode

from httpx import Client

from .. import types
from .. import errors


log = logging.getLogger('proxy6')


class APIConnector:
    ENDPOINT = 'https://proxy6.net/api/{}/{}'

    def __init__(self, apikey: str) -> None:
        self.apikey = apikey
        self.__rps_try = 0

    def make_request(self, method: str, params: dict | None = None) -> dict:
        '''Makes API request.

        Args:
            method (str): API method.
            params (dict | None, optional): API params. Defaults to None.

        Raises:
            errors.RPSAPIError: RPS error.
            errors.UnexpectedAPIError: API unexpected error.

        Returns:
            dict: API response.
        '''
        log.debug(f'Called with args: ({method}, {params}); Try #{self.__rps_try}.')
        sleep(1)  # skip RPS error... Maybe...
        url = self.ENDPOINT.format(self.apikey, method)
        if params:
            url += f'?{urlencode(params)}'
        log.debug(f'Final URL: {url}')
        with Client() as sess:
            resp = sess.get(url)
            if resp.is_success:
                json_resp = resp.json()
                log.debug(f'API Response: {json_resp}')
                return self.process_api_response(json_resp)
            elif resp.status_code == 503:
                if self.__rps_try == 3:
                    self.__rps_try = 0
                    raise errors.RPSAPIError('Большое колличество запросов. Попробуйте позже.')
                self.__rps_try += 1
                return self.make_request(method, params)
            else:
                raise errors.UnexpectedAPIError('Не удалось получит данные у API.')

    def process_api_response(self, resp: dict) -> dict:
        '''Checking API response on errors. If not - returns response.

        Args:
            resp (dict): API response.

        Raises:
            errors.UnknownAPIError: API unknown error.
            errors.KeyAPIError: API unauthorized error.
            errors.MethodAPIError: API method unexists.
            errors.CountAPIError: API count error.
            errors.PeriodAPIError: API period error.
            errors.CountryAPIError: API country error.
            errors.IDsAPIError: API IDs error.
            errors.DescrAPIError: API descr error.
            errors.TypeAPIError: API type error.
            errors.ActiveProxyAllowAPIError: API active proxy allow error.
            errors.NoMoneyAPIError: API no money error.
            errors.NotFoundAPIError: API not found error.
            errors.PriceAPIError: API price error.
            errors.UnexpectedAPIError: API unexpected error.

        Returns:
            dict: API response.
        '''
        log.debug(f'Called with args: ({resp})')
        if resp.get('error'):
            match resp.get('error_id'):
                case 30:
                    raise errors.UnknownAPIError(
                        resp, resp.get('error', 'Неизвестная ошибка')
                    )
                case 100:
                    raise errors.KeyAPIError(
                        resp, 'Ошибка авторизации, неверный ключ'
                    )
                case 110:
                    raise errors.MethodAPIError(
                        resp, 'Ошибочный метод'
                    )
                case 200:
                    raise errors.CountAPIError(
                        resp, 'Ошибка кол-ва прокси, неверно указано кол-во, либо отсутствует'
                    )
                case 210:
                    raise errors.PeriodAPIError(
                        resp, 'Ошибка периода, неверно указано кол-во (дней), либо отсутствует'
                    )
                case 220:
                    raise errors.CountryAPIError(
                        resp, 'Ошибка страны, неверно указана страна (страны указываются в формате iso2), либо отсутствует'
                    )
                case 230:
                    raise errors.IDsAPIError(
                        resp, 'Ошибка списка номеров прокси. Номера прокси должны быть указаны через запятую'
                    )
                case 250:
                    raise errors.DescrAPIError(
                        resp, 'Ошибка технического комментария, неверно указан, либо отсутствует'
                    )
                case 260:
                    raise errors.TypeAPIError(
                        resp, 'Ошибка типа (протокола) прокси, неверно указан, либо отсутствует'
                    )
                case 300:
                    raise errors.ActiveProxyAllowAPIError(
                        resp, 'Ошибка кол-ва прокси. Возникает при попытке покупки большего кол-ва прокси, чем доступно на сервисе'
                    )
                case 400:
                    raise errors.NoMoneyAPIError(
                        resp, 'Ошибка баланса. На вашем балансе отсутствуют средства, либо их не хватает для покупки запрашиваемого кол-ва прокси'
                    )
                case 404:
                    raise errors.NotFoundAPIError(
                        resp, 'Ошибка поиска. Возникает когда запрашиваемый элемент не найден'
                    )
                case 410:
                    raise errors.PriceAPIError(
                        resp, 'Ошибка расчета стоимости. Итоговая стоимость меньше, либо равна нулю'
                    )
                case _:
                    raise errors.UnexpectedAPIError(
                        resp, resp.get(
                            'error',
                            'Неожиданная ошибка API'
                        )
                    )
        else:
            return resp


class Proxy6(APIConnector):
    def __init__(self, apikey: str) -> None:
        super().__init__(apikey)

    def get_price(
        self, count: int,
        period: int, version: types.ProxyVersion = types.ProxyVersion.IPV6
    ) -> types.GetPriceResponse:
        '''Используется для получения информации о сумме заказа в зависимости от периода и кол-ва прокси.

        Args:
            count (int): Кол-во прокси.
            period (int): Период - кол-во дней
            version (types.ProxyVersion): Версия прокси. Стандартно - types.ProxyVersion.IPV6

        Returns:
            types.GetPriceResponse: Ответ API.
        '''
        log.debug(f'Called with args: ({count}, {period}, {version})')
        params = {
            'count': count, 'period': period,
            'version': version.value
        }
        resp = self.make_request('getprice', params)
        return types.GetPriceResponse(**resp)

    def get_count(
        self, country: str, version: types.ProxyVersion = types.ProxyVersion.IPV6
    ) -> types.GetCountResponse:
        '''Используется для получения информации о доступном для приобретения кол-ве прокси определенной страны.

        Args:
            country (str): Код страны в формате iso2.
            version (types.ProxyVersion): Версия прокси. Стандартно - types.ProxyVersion.IPV6

        Returns:
            types.GetCountResponse: Ответ API.
        '''
        log.debug(f'Called with args: ({country}, {version})')
        params = {
            'country': country, 'version': version.value
        }
        resp = self.make_request('getcount', params)
        return types.GetCountResponse(**resp)

    def get_country(
        self, version: types.ProxyVersion = types.ProxyVersion.IPV6
    ) -> types.GetCountryResponse:
        '''Используется для получения информации о доступных для приобретения странах.

        Args:
            version (types.ProxyVersion, optional): Версия прокси. Defaults to types.ProxyVersion.IPV6.

        Returns:
            types.GetCountryResponse: Ответ API.
        '''
        log.debug(f'Called with args: ({version})')
        resp = self.make_request(
            'getcountry', {'version': version.value}
        )
        return types.GetCountryResponse(**resp)

    def get_proxy(
        self, state: types.ProxyState = types.ProxyState.ALL,
        descr: str | None = None
    ) -> types.GetProxyResponse:
        '''Используется для получения списка ваших прокси.

        Args:
            state (types.ProxyState, optional): Состояние возвращаемых прокси. Доступные значения: active - Активные, expired - Неактивные, expiring - Заканчивающиеся, all - Все (по-умолчанию). Defaults to types.ProxyState.ALL.
            descr (str | None, optional): Технический комментарий, который вы указывали при покупке прокси. Если данный параметр присутствует, то будут выбраны только те прокси, у которых присутствует данный комментарий, если же данный параметр не задан, то будут выбраны все прокси. Defaults to None.

        Returns:
            types.GetProxyResponse: Ответ API.
        '''
        log.debug(f'Called with args: ({state}, {descr})')
        params = {
            'state': state.value
        }
        if descr:
            params['descr'] = descr
        resp = self.make_request('getproxy', params)
        return types.GetProxyResponse(**resp)

    def set_type(
        self, ids: list[str], type: types.ProxyType
    ) -> types.SetTypeResponse:
        '''Используется для изменения типа (протокола) у списка прокси.

        Args:
            ids (list[str]): Перечень внутренних номеров прокси в нашей системе;
            type (types.ProxyType): Устанавливаемый тип (протокол).

        Returns:
            types.SetTypeResponse: Ответ API.

        Note:
            В случае, если ВСЕ прокси, у которых вы хотите изменить тип (переданные через параметр ids), уже имеют соответствующий тип (протокол), то вернется ошибочный ответ с номером 30 (Error unknown).
        '''
        log.debug(f'Called with args: ({ids}, {type})')
        params = {
            'ids': ','.join(ids),
            'type': type.value
        }
        resp = self.make_request('settype', params)
        return types.SetTypeResponse(**resp)

    def set_descr(
        self, new: str, old: str | None = None,
        ids: list[str] | None = None
    ) -> types.SetDescrResponse:
        '''Используется для обновления технического комментария у списка прокси, который был установлен при покупке.

        Args:
            new (str): Технический комментарий, на который нужно изменить. Максимальная длина 50 символов.
            old (str | None, optional): Технический комментарий, который нужно изменить. Defaults to None.
            ids (list[str] | None, optional): Перечень внутренних номеров прокси в нашей системе. Defaults to None.

        Returns:
            types.SetDescrResponse: Ответ API.

        Raises:
            TypeError: Отсутствует один из обязательных аргументов: "old" или "ids".
            ValueError: Аргумент "new" превышает максимальную длину в 50 символов.

        Note:
            Обязательно должен присутствовать один из параметров, либо `ids`, либо `old`.
        '''
        if not old and not ids:
            raise TypeError('Обязательно должен быть указан один из аргументов: "old" или "ids"')
        elif len(new) <= 0 or len(new) > 50:
            raise ValueError(
                'Аргумент "new" превышает максимальную длину в 50 символов.'
            )
        else:
            params = {
                'new': new
            }
            if old:
                params['old'] = old
            if ids:
                params['ids'] = ','.join(ids)
            resp = self.make_request('setdescr', params)
            return types.SetDescrResponse(**resp)

    def buy(
        self, count: int, period: int, country: str,
        version: types.ProxyVersion = types.ProxyVersion.IPV6,
        type: types.ProxyType = types.ProxyType.HTTPS,
        descr: str | None = None, auto_prolong: bool = False
    ) -> types.BuyResponse:
        '''Используется для покупки прокси.

        Args:
            count (int): Кол-во прокси для покупки.
            period (int): Период на который покупаются прокси - кол-во дней.
            country (str): Страна в формате iso2.
            version (types.ProxyVersion, optional): Страна в формате iso2. Defaults to types.ProxyVersion.IPV6.
            type (types.ProxyType, optional): Тип прокси (протокол). Defaults to types.ProxyType.HTTPS.
            descr (str | None, optional): Технический комментарий для списка прокси, максимальная длина 50 символов. Указание данного параметра позволит вам делать выборку списка прокси про этому параметру через метод `getproxy`. Defaults to None.
            auto_prolong (bool, optional): При добавлении данного параметра, у купленных прокси будет включено автопродление. Defaults to False.

        Returns:
            types.BuyResponse: Ответ API.

        Raises:
            ValueError: Аргумент "descr" превышает максимальную длину в 50 символов.
        '''
        log.debug(f'Called with args: ({count}, {period}, {country}, {version}, {type}, {descr}, {auto_prolong})')
        params = {
            'count': count,
            'period': period,
            'country': country,
            'version': version.value,
            'type': type.value
        }
        if descr:
            if len(descr) <= 0 or len(descr) > 50:
                raise ValueError(
                    'Аргумент "descr" превышает максимальную длину в 50 символов.'
                )
            else:
                params['descr'] = descr
        if auto_prolong:
            params['auto_prolong'] = ''
        resp = self.make_request('buy', params)
        return types.BuyResponse(**resp)

    def prolong(
        self, period: int, ids: list[str]
    ) -> types.ProlongResponse:
        '''Используется для продления текущих прокси.

        Args:
            period (int):  Период продления - кол-во дней.
            ids (list[str]): Перечень внутренних номеров прокси в нашей системе.

        Returns:
            types.ProlongResponse: Ответ API.
        '''
        log.debug(f'Called with args: ({period}, {ids})')
        params = {
            'period': period,
            'ids': ','.join(ids)
        }
        resp = self.make_request('prolong', params)
        return types.ProlongResponse(**resp)

    def delete(
        self, ids: list[str] | None = None, descr: str | None = None
    ) -> types.DeleteResponse:
        '''Используется для удаления прокси.

        Args:
            ids (list[str] | None, optional): Перечень внутренних номеров прокси в нашей системе. Defaults to None.
            descr (str | None, optional): Технический комментарий, который вы указывали при покупке прокси, либо через метод `setdescr`. Defaults to None.

        Returns:
            types.DeleteResponse: Ответ API.

        Raises:
            TypeError: Обязательно должен быть указан один из аргументов: "ids" или "descr".

        Note:
            Обязательно должен присутствовать один из параметров, либо `ids`, либо `descr`.
        '''
        log.debug(f'Called with args: ({ids}, {descr})')
        if not ids or not descr:
            raise TypeError(
                'Обязательно должен быть указан один из аргументов: "ids" или "descr"'
            )
        if ids:
            params = {'ids': ','.join(ids)}
        else:
            params = {'descr': descr}
        resp = self.make_request('delete', params)
        return types.DeleteResponse(**resp)

    def check(self, ids: str) -> types.CheckResponse:
        '''Используется для проверки валидности (работоспособности) прокси.

        Args:
            ids (str): Внутренний номер прокси в нашей системе.

        Returns:
            types.CheckResponse: Ответ API.
        '''
        log.debug(f'Called with args: ({ids})')
        resp = self.make_request(
            'check', {'ids': ids}
        )
        return types.CheckResponse(**resp)

    def ipauth(self, ip: list[str] | None = None, delete: bool = False) -> types.IPAuthResponse:
        '''Используется для привязки, либо удаления авторизации прокси по ip.

        Args:
            ip (list[str] | None): Список привязываемых ip-адресов. Defaults is None.
            delete (bool): Удалить привязку по IP? Defaults is False.

        Returns:
            types.IPAuthResponse: Ответ API.

        Raises:
            TypeError: Указаны оба аргумента: "ip" и "delete".

        Note:
            Может быть использован только 1 аргумент: "ip" или "delete".
        '''
        log.debug(f'Called with args: ({ip}, {delete})')
        if ip and delete:
            raise TypeError('Указаны оба аргумента: "ip" и "delete"')
        if ip:
            params = {
                'ip': ','.join(ip)
            }
        else:
            params = {
                'ip': 'delete'
            }
        resp = self.make_request('ipauth', params)
        return types.IPAuthResponse(**resp)
