# -*- coding: utf-8 -*-
#
#  pyProxy6 API: Types
#  Created by LulzLoL231 at 02/07/22
#
from typing import Dict, List
from decimal import Decimal
from datetime import datetime
from enum import Enum, IntEnum
from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field


class ProxyVersion(IntEnum):
    IPV6 = 6
    IPV4 = 4
    IPV4_SHARED = 3


class ProxyType(Enum):
    HTTPS = 'http'
    SOCKS5 = 'socks'


class ProxyState(Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    EXPIRING = 'expiring'
    ALL = 'all'


class BaseAPIResponse(BaseModel):
    '''Эти данные всегда возвращаются при успешном ответе от API.
    '''
    status: str = Field(
        'yes', description='Всегда "yes", если успешный ответ и не возникло ошибок'
    )
    user_id: str = Field(
        ..., description='Номер вашего аккаунта'
    )
    balance: Decimal = Field(
        ..., description='Текущее состояние вашего баланса'
    )
    currency: str = Field(
        ..., description='Валюта вашего аккаунта (RUB, либо USD)'
    )


class GetPriceResponse(BaseAPIResponse):
    price: Decimal = Field(..., description='Итоговая стоимость')
    price_single: Decimal = Field(
        ..., description='Стоимость одного прокси'
    )
    period: int = Field(
        ..., description='Запрошенный период (кол-во дней)'
    )
    count: int = Field(..., description='Запрошенное кол-во прокси')


class GetCountResponse(BaseAPIResponse):
    count: int = Field(..., description='Доступное кол-во')


class GetCountryResponse(BaseAPIResponse):
    list: List[str] = Field(
        ..., description='Массив доступных стран в формате ISO2'
    )


class ProxyInfo(BaseModel):
    id: str = Field(
        ..., description='Внутренний номер прокси'
    )
    ip: IPv4Address | IPv6Address = Field(
        ..., description='IPv4, либо IPv6'
    )
    host: str = Field(..., description='Хост прокси')
    port: int = Field(..., description='Порт прокси')
    user: str = Field(..., description='Логин')
    passwd: str = Field(
        ..., alias='pass', description='Пароль'
    )
    version: ProxyVersion = Field(
        ..., description='Версия прокси'
    )
    type: ProxyType = Field(
        ..., description='Тип прокси'
    )
    country: str | None = Field(
        None, description='Страна прокси в формате ISO2'
    )
    date: datetime = Field(
        ..., description='Дата покупки прокси'
    )
    date_end: datetime = Field(
        ..., description='Дата окончания срока действия прокси'
    )
    descr: str | None = Field(
        None, description='Технический комментарий'
    )
    active: bool = Field(
        ..., description='Прокси активен или нет'
    )

    def get_uri(self) -> str:
        '''Makes URI.

        Returns:
            str: URI.
        '''
        if self.type == ProxyType.HTTPS:
            return f'https://{self.user}:{self.passwd}@{self.host}:{self.port}'
        else:
            return f'socks5://{self.user}:{self.passwd}@{self.host}:{self.port}'


class GetProxyResponse(BaseAPIResponse):
    list_count: int = Field(
        ..., description='Кол-во прокси'
    )
    list: Dict[str, ProxyInfo] = Field(
        ..., description='Массив прокси'
    )


SetTypeResponse = BaseAPIResponse


class SetDescrResponse(BaseAPIResponse):
    count: int = Field(
        ..., description='Кол-во прокси у которых был изменен комментарий'
    )


class BuyResponse(BaseAPIResponse):
    count: int = Field(
        ..., description='Запрошенное кол-во прокси для покупки'
    )
    period: int = Field(
        ..., description='Запрошенный период для покупки (кол-во дней)'
    )
    country: str = Field(
        ..., description='Локация (страна) прокси для покупки в формате ISO2'
    )
    list: Dict[str, ProxyInfo] = Field(
        ..., description='Массив купленных прокси'
    )


class ProxyProlongInfo(BaseModel):
    id: str = Field(
        ..., description='Внутренний номер прокси'
    )
    date_end: datetime = Field(
        ..., description='Новая дата окончания срока действия прокси'
    )


class ProlongResponse(BaseAPIResponse):
    price: Decimal = Field(
        ..., description='Итоговая стоимость продления'
    )
    price_single: Decimal | None = Field(
        None, description='Стоимость одного прокси для указанного кол-ва и периода (отсутствует при продлении смешанного типа прокси)'
    )
    period: int = Field(
        ..., description='Запрошенный период для продления (кол-во дней)'
    )
    count: int = Field(
        ..., description='Кол-во успешных продлений'
    )
    list: Dict[str, ProxyProlongInfo] = Field(
        ..., description='Массив продленных прокси'
    )


class DeleteResponse(BaseAPIResponse):
    count: int = Field(
        ..., description='Кол-во удаленных прокси'
    )


class CheckResponse(BaseAPIResponse):
    proxy_id: str = Field(
        ..., description='Внутренник номер прокси'
    )
    proxy_status: bool = Field(
        ..., description='Результат проверки'
    )


IPAuthResponse = BaseAPIResponse
