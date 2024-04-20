from rest_framework import status
from rest_framework.response import Response

class BaseServiceException(Exception):
    detail = 'Неизвестная ошибка'

    def __init__(self, detail: str, *args) -> None:
        super().__init__(*args)
        self.detail = detail

    def response(self):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'detail': self.detail}
        )