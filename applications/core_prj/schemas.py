from typing import Dict, List, Union
from ninja import Schema


class TimeEventContract(Schema):
    name: Union[str, None]
