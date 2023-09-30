from bson import ObjectId
from pydantic_core import core_schema
from typing import Annotated, Any

from pydantic.json_schema import JsonSchemaValue
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
        cls.validate_object_id, 
        core_schema.str_schema(), 
        serialization=core_schema.to_string_ser_schema(),
    )

    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())