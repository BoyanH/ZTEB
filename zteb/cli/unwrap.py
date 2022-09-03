"""
Command Line Interface For Unwrapping A Birthday-Card.
"""


import importlib.resources as pkg_resources
from typing import Optional
import click
from zteb import cards
from zteb.crypto import TimeLockPuzzle


DEFAULT_CARD_NAME = 'tony-birthday-card.zteb'


@click.command()
@click.option(
    '-c', '--card',
    type=click.Path(exists=True, writable=True, readable=True),
    help=("Path to a wrapped birthday-card. If not specified, the built-in"
          "card for Tony's birthday is being unwrapped."),
)
@click.option(
    '-o', '--output-file',
    type=click.Path(writable=True),
    help='Path to file to store card message to.',
)
@click.option(
    '-s', '--silent',
    type=click.BOOL,
    is_flag=True,
    help='Suppress all stdout output.',
)
def unwrap(
        card: str,
        output_file: str,
        silent: bool,
):
    """
    Unwrap an electronic birthday-card.
    """
    puzzle_bytes = get_card_bytes(card)
    puzzle = TimeLockPuzzle.load(puzzle_bytes)

    if puzzle.is_solved:
        deliver_message(puzzle.solution, output_file, silent)
        return

    if not silent and puzzle.instructions:
        print(puzzle.instructions)

    try:
        puzzle.solve(show_progress=not silent)
        deliver_message(puzzle.solution, output_file, silent)
    except KeyboardInterrupt:
        if not silent:
            print(
                "Your card wasn't completely unwrapped, "
                "but you can continue at any time!"
            )
    finally:
        puzzle_state = puzzle.dump()
        store_card_bytes(card, puzzle_state)


def deliver_message(
        message: str,
        output_file: Optional[str] = None,
        silent: bool = True):
    """
    Delivers the card message to the user,
    i.e. prints it to stdout if not in silent mode
    and outputs it to a file if provided.
    """
    if not silent:
        print(message)

    if output_file:
        with open(output_file, 'w', encoding='utf8') as file:
            file.write(message)


def get_card_bytes(card_path: Optional[str]) -> bytes:
    """
    Retrieves the card data from the given card_path
    or the default card if missing.
    """
    if not card_path:
        return pkg_resources.read_binary(cards, DEFAULT_CARD_NAME)

    with open(card_path, 'rb') as file:
        return file.read()


def store_card_bytes(card_path: Optional[str], data: bytes):
    """
    Stores the card data to the given card_path or the default
    card path if missing.
    """
    def open_():
        if card_path:
            return open(card_path, 'wb')

        with pkg_resources.path(cards, DEFAULT_CARD_NAME) as p:
            return open(p, 'wb')

    with open_() as file:
        file.write(data)
