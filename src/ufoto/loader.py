"""Load model directories as packages."""

import importlib
import pathlib
import site
from typing import Union


def load_model(path: Union[str, pathlib.Path]):
  mod_path = pathlib.Path(str(path))
  pkg_path = mod_path.parent

  site.addsitedir(pkg_path)
  site.addsitedir(mod_path)

  stem = mod_path.stem
  try:
    model = importlib.import_module(stem)
  except ModuleNotFoundError as exc:
    print(exc)
    return None
  else:
    return model
