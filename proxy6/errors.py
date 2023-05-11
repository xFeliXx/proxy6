# -*- coding: utf-8 -*-
#
#  pyProxy6 API: Errors
#  Created by LulzLoL231 at 02/07/22
#
class BaseAPIError(Exception):
    def __init__(self, raw_response: dict, *args: object) -> None:
        super().__init__(*args)
        self.raw_response = raw_response


class UnexpectedAPIError(Exception):
    pass


class RPSAPIError(Exception):
    pass


class UnknownAPIError(BaseAPIError):
    pass


class KeyAPIError(BaseAPIError):
    pass


class MethodAPIError(BaseAPIError):
    pass


class CountAPIError(BaseAPIError):
    pass


class PeriodAPIError(BaseAPIError):
    pass


class CountryAPIError(BaseAPIError):
    pass


class IDsAPIError(BaseAPIError):
    pass


class DescrAPIError(BaseAPIError):
    pass


class TypeAPIError(BaseAPIError):
    pass


class ActiveProxyAllowAPIError(BaseAPIError):
    pass


class NoMoneyAPIError(BaseAPIError):
    pass


class NotFoundAPIError(BaseAPIError):
    pass


class PriceAPIError(BaseAPIError):
    pass
