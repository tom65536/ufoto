"""Methods for writing the model."""
import enum
import json
from pathlib import Path
from typing import (
    Any,
    Dict,
    IO,
    Mapping,
    Sequence,
    Union,
)

import cbor2
import toml
import yaml


class OutputFormat(enum.Enum):
  """
  The implemented formats for output.

  :param mode: the file mode for opening a file for writing
  :type mode: str
  :param dump_fn: method for dumping to a stream in the given format
  :type dump_fn: Callable[[IO, Mapping[str, Any]], None]
  :param suffixes: List of file suffixes mapped to this type
  :type suffixes: Sequence[str]
  """
  CBOR = ('wb', cbor.dump, ('.cbor', '.cbr'))
  JSON = ('w', json.dump, ('.json', '.jsn'))
  TOML= ('w', toml.dump, ('.toml', '.tml'))
  YAML = ('w', yaml.dump, ('.yaml', '.yml'))

  def __init__(self,
      mode: str,
      dump_fn: Callable[[IO, Mapping[str, Any]], None],
      suffixes: Sequence[str],
  ) -> None:
    """Initialize a new instance."""
    self._mode = mode
    self._dump_fn = dump_fn
    self._suffixes = suffixes

  @property
  def mode(self) -> str:
    """Return the file mode for opening a file for writing."""
    return self._mode

  def get_default_suffix(self) -> str:
    """Return a default file suffix."""
    return self._suffixes[0]

  @property
  def suffixes(self) -> Sequence[str]:
    """Return the suffixes associated with this type."""

  def dump(self, stream: IO, structure: Mapping[str, Any]) -> None:
    """
    Write a given ``structure`` to a ``stream`` in serialized form.

    :param stream: the stream to write to
    :type stream: IO
    :param structure: the structure to be written in serialized form
    :type structure: Dict[str, Any]
    """
    self._dump_fn(stream, structure)

  @staticmethod
  def for_file(path_like: Union[str, Path]) -> 'OutputFormat':
    """
    Obtain an output format for a given path like object.

    :param path_like: a string or path object pointing to a file name
    :type path_like: Union[str, Path]
    :return: the associated output format or `OutputFormat.JSON` if no type is associated at all.
    :rtype: OutputFormat
    """
    path = Path(str(path_like))
    suffix = path.suffix.lower()

    for output_format in OutputFormat:
      if suffix in output_format.suffixes:
        return output_format
    return OutpuFormat.JSON

