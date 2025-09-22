"""
file		: utils
description	:
"""
import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Union
from .common import PKG_NAME
from urllib.parse import urlparse


logger = logging.getLogger(f"{PKG_NAME}.utl")


def resource_path(relative_path: Union[str, Path]) -> os.path:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    :param relative_path: relative_path need to convert to absolute path
    :return: the absolute path
    """
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.getcwd()
    _rp = os.path.join(base_path, relative_path)
    # os.makedirs(_rp, exist_ok=True)
    return _rp


def compress_folder(base_name: str, root_dir: Union[str, Path]) -> bool:
    """
    :param base_name:  is the name of the file to create, minus any format-specific
    extension; The extension default is ".zip"
    :param root_dir: is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.
    :return: True / False
    """
    try:
        shutil.make_archive(base_name, format='zip', root_dir=root_dir)
        return True
    except Exception as e:
        logger.error(f"Compress failed: {e}")
        return False


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
