from typing import Dict, List, Any

from typing import Union
from ninja import Schema


class TimeEventContract(Schema):
    name: Union[str, None]


class OkResponseContract(Schema):
    ok: bool


class MsgResponseContract(Schema):
    message: str


class FormInvalidResponseContract(Schema):
    errors: Dict[str, List[Dict[str, Any]]]


class OkDataResponseContract(Schema):
    ok: bool
    data: Union[Dict, List]
