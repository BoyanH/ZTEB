"""
Command Line Interface For Wrapping A Birthday-Card.
"""


from datetime import timedelta
import click
from zteb.crypto import TimeLockPuzzle
from .argtype import TimeDeltaParamType


@click.command()
@click.argument(
    'card',
    type=click.Path(exists=True, readable=True),
)
@click.argument(
    'output',
    type=click.Path(writable=True),
)
@click.option(
    '-w', '--wrapper-text',
    type=click.Path(exists=True, readable=True),
    help=('Optional path to file containing wrapper text. '
          'This is shown while unwrapping the card.'),
)
@click.option(
    '-d', '--duration',
    type=TimeDeltaParamType(),
    help=('Desired amount of time for the unwrapping to take '
          'in the format of pandas.Timedelta. (Default = 7h)'),
)
def wrap(
        card: str,
        output: str,
        wrapper_text: str,
        duration: timedelta,
):
    """
    Wrap an electronic birthday-card.
    """
    if duration is None:
        duration = timedelta(hours=7)

    puzzle = TimeLockPuzzle.generate(
        solution=get_file_content(card),
        instructions=get_file_content(wrapper_text) if wrapper_text else None,
        desired_duration=duration
    )
    dump = puzzle.dump()

    with open(output, 'wb') as file:
        file.write(dump)


def get_file_content(file_name: str, encoding: str = 'utf8'):
    with open(file_name, 'r', encoding=encoding) as file:
        return file.read()
