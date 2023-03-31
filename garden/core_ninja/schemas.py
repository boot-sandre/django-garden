from typing import Dict, List, Any

from typing import Union
from ninja import Schema


class SuccessResponseContract(Schema):
    success: bool
    message: Union[str, None]
