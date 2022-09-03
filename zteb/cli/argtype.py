"""
Contains custom arguments for the command line interface.
"""


import pandas as pd
import click


class TimeDeltaParamType(click.ParamType):
    """
    Time delta argument in the format of pandas.Timedelta.
    """
    name = "delta"

    # pylint doesn't know that self.fail raises
    # pylint: disable=inconsistent-return-statements

    def convert(self, value, param, ctx):

        try:
            pandas_delta = pd.Timedelta(value)
            return pandas_delta.to_pytimedelta()
        except (TypeError, ValueError):
            self.fail(
                (f'{value!r} is not a valid time delta '
                 'in the format of pandas.Timedelta.'),
                param, ctx,
            )
