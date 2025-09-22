"""
file		: adapter
create date	: 15 Nov, 2023 
description	:
"""
import os
import sys
import json
import logging
from pathlib import Path
from typing import Union
from .common import PKG_NAME
from .schemas import OutputObject, InputObject, ErrorMsg, FileObject

logger = logging.getLogger(f"{PKG_NAME}.adapter")


def dict_to_inputObj(json_pth: Union[str, Path]) -> InputObject:
    """
    Convert json data to InputObject
    :param json_pth: path to JSON file, storing input params
    :return: an InputObject, This object is input to <AI-lib>.run()
    """
    with open(json_pth, "r") as fr:
        json_data = json.load(fr)
    input_obj = InputObject.model_validate(json_data)
    return input_obj


def outputObj_to_dict(output_obj: OutputObject, tmp_dir: Union[str, Path]) -> dict:
    """
    Convert OutputObject to dict, write all BufferedReader in "files" to local file
    :param output_obj: OutputObject, result from AI-task
    :param tmp_dir: temporary directory storage file, tmp_dir will be deleted after the AI-task done
    :return: dict
    """
    for k, v in output_obj:
        # write buff to local
        if isinstance(v, FileObject):
            v.write_buff(tmp_dir=tmp_dir)
    return output_obj.model_dump()


def make_output(output_obj: OutputObject, tmp_dir: Union[str, Path] = None):
    """Convert OutputObject to dict, then print output to console when run exe file,
    aioz-ai-node modules will be capture it and
    """
    output_dict = {}
    key_files = []
    for k, v in output_obj:
        if isinstance(v, FileObject):
            key_files.append(k)
            output_dict[k] = v.write_buff(tmp_dir)
        elif isinstance(v, list) and all(isinstance(elem, FileObject) for elem in v):
            key_files.append(k)
            lst = [elem.write_buff(tmp_dir) for elem in v]
            output_dict[k] = lst
        else:
            output_dict[k] = v
    output_dict["key_files"] = key_files
    print(output_dict, file=sys.stdout)


def make_error(msg: str, traceback: str = ""):
    error_obj = ErrorMsg(message=msg, traceback=traceback)
    print(error_obj.model_dump(), file=sys.stdout)

