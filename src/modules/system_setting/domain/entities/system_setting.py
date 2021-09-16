from pydantic.class_validators import root_validator, validator
from typing import Union
from pydantic import Field, BaseModel

from addict import Addict

from core.base_classes.entity import Entity
from core.value_objects import DateVO, ID

from typing import get_args


class SystemSettingProps(BaseModel):

    editor_id: ID
    max_translate_text_per_day: int = Field(...)
    max_translate_doc_per_day: int = Field(...)
    translation_history_expire_duration: int = Field(...)

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def validate(cls, values):
        return values


class SystemSettingEntity(Entity[SystemSettingProps]):
    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    pass
