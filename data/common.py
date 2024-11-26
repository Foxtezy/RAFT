from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class NodeId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source: type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.str_schema()