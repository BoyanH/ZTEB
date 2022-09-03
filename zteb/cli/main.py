"""
Main Command Line Interface Entry Point.
"""


import click
from .wrap import wrap
from .unwrap import unwrap


@click.group()
def cli_group():
    """
    ZTEB is Tony's Electronic Birthday-card (ZTEB).
    It can wrap (quite tightly) or unwrap an electronic birthday card.
    A desired amount of time for the unwrapping to take can be specified
    when wrapping a card. The real unwrapping duration, however, can
    vary greatly on various machines.

    Since this is Tony's card, after all, just calling `zteb unwrap`
    unwraps his card.
    """


cli_group.add_command(wrap)
cli_group.add_command(unwrap)
