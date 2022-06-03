from typing import Optional, AnyStr, Any, Union, List, Dict
from pydantic import BaseModel
import json

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

class User(BaseModel):
    username: str
    email: str
    password: str
