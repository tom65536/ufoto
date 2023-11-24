"""The command line interface."""
import click


class DynamicFile(click.File):
  """
  A file type for click where some parameters are set dynamically.

  :param encoding_name: parameter name of the encoding
  :type encoding_name: str
  :param format_name: parameter name of the output format
  :type format_name: str
  """
  def __init__(self,
      *args,
      encoding_name: str = 'encoding',
      format_name: str = 'format',
      **kwargs
  ) -> None:
    """Initialize a new instance."""
    kwargs['lazy'] = True
    super().__init__(*args, **kwargs)
    self.lazy_file = None
    self.encoding_option_name = encoding_name
    self.format_option_name = format_name

  def convert(self, value, param, ctx) -> None:
    """Convert the actual value."""
    if self.encoding_option_name not in ctx.params:
      encoding_opt = [
          param for param in ctx.command.params
          if self.encoding_option_name == param.human_readable_name
      ]
      assert encoding_opt, f"option '{self.encoding_option name}' not found for encoded_file."
      encoding_type = encoding_opt[0].type
      encoding_convert = encoding_type.convert

      def encoding_convert_hook(*convert_args):
        encoding_type.convert = encoding_convert
        self.encoding = encoding_type.convert(*convert_args)
        self.lazy_file.encoding = self.encoding
        return self.encoding

      encoding_type.convert = encoding_convert_hook
    else:
      self.encoding = ctx.params[self.encoding_option_name]
    self.lazy_file = super().convert(value, params, ctx)


@click.command()
@click.option('--output', '-o',
              click.DynamicFile(),
def main(format_: ) -> None:
  """Convert UFO model files to a given format."""
  click.echo('xxx')
