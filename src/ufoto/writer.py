"""Methods for writing the model."""
import enum
import json
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Mapping,
    Sequence
)

import cbor2
import toml
import yaml


class OutputFormat(enum.Enum):
  """The implemented formats for output."""
  CBOR = enum.auto()
  JSON = enum.auto()
  TOML= enum.auto()
  YAML = enum.auto()

def get_writer(
    fmt: OutputFormat
) -> Callable[[IO, Mapping[str, Any]], None]:
  """
  Return a writer serializing to the given format.

  The writer takes a structure and a file like
  object as arguments.

  :param fmt: the output format
  :type fmt: OutputFormat
  :return: the writer
  :rtype: Callable[[Mapping[str, Any], IO], None]
  """
  if fmt == OutputFormat.CBOR:
    return cbor2.dump
  if fmt == OutputFormat.JSON:
    return json.dump
  if fmt == OutputFormat.YAML:
    return yaml.dump
  if fmt == OutputFormat.TOML:
    return toml.dump
  raise NotImplementedError()

def get_mode(
    fmt: OutputFormat
) -> str:
  """
  Return the file mode required for the given format.

  The mode may be ``'b'`` for binary or ``''``
  for text mode.

  :param fmt: the output format
  :type fmt: OutputFormat
  :return:  ``'b'`` for binary or ``''`` for text mode
  :rtype: str
  """
  if fmt == OutputFormat.CBOR:
    return 'b'
  return ''
