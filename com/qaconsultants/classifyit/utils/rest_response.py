import typing


class RestResponse:
    def __init__(self) -> None:
        super().__init__()
        self.status = -1
        self.body = ""

    def set_status(self, status: int):
        self.status = status

    def set_body(self, body: typing.List[typing.Dict]):
        self.body = body

    def set_status_and_body(self,status: int, body: typing.List[typing.Dict]):
        self.status = status
        self.body = body
