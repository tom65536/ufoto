"""The command line interface."""
import click


@click.command()
@click.option('--output', '-o',
              click.File('wb'),
def main(format_: ) -> None:
  """Convert UFO model files to a given format."""
  click.echo('xxx')
