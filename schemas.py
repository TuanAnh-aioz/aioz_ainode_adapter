"""
file		: schemas
description	:
"""
import os
import io
import tempfile
from . import utils
from pathlib import Path
from typing import Literal, List, Union
from pydantic import BaseModel, ConfigDict, AnyUrl


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        protected_namespaces=())

    @property
    def type_name(self):
        return self.type


class FileObject(CustomBaseModel):
    type: Literal["FileObj"] = "FileObj"
    data: Union[io.BufferedReader, Path, AnyUrl] = None
    name: str = "output_file.ext"

    def write_buff(self, tmp_dir: Union[str, Path] = None):
        if tmp_dir and os.path.isdir(tmp_dir):
            fd, fp = tempfile.mkstemp(dir=tmp_dir, suffix=self.name)
        else:
            fd, fp = tempfile.mkstemp(suffix=self.name)
        if isinstance(self.data, io.BufferedReader):
            with open(fp, "wb") as fw:
                fw.write(self.data.read())
            self.data = Path(fp)
        return str(self.data)


class InputObject(CustomBaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["InputObj"] = "InputObj"
    device: Literal["cpu", "cuda", "gpu"] = "cuda"
    model_storage_directory: str = utils.resource_path("models")


class OutputObject(CustomBaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["OutputObj"] = "OutputObj"


class ErrorMsg(CustomBaseModel):
    type: Literal["ErrorMsg"] = "ErrorMsg"
    message: str = "Something went wrong"
    traceback: str = ""

