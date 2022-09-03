"""
Fixtures for testing the functionality in the crypto module.
"""


import datetime
import multiprocessing
import time
import os
import signal
import pytest
from zteb.crypto import TimeLockPuzzle


@pytest.fixture
def message():
    return "Dem secrets."


@pytest.fixture
def puzzle_duration() -> datetime.timedelta:
    return datetime.timedelta(seconds=2)


@pytest.fixture
def puzzle(
        message: str,
        puzzle_duration: datetime.timedelta
) -> TimeLockPuzzle:
    return TimeLockPuzzle.generate(
        message,
        instructions='Some instructions...',
        desired_duration=puzzle_duration,
    )


def start_solving_and_interrupt(puzzle: TimeLockPuzzle) -> TimeLockPuzzle:
    def solve_ignore_interrupt(communication_channel):
        try:
            puzzle.solve()
        except KeyboardInterrupt:
            communication_channel.put(puzzle)

    queue = multiprocessing.Queue()
    solver_process = multiprocessing.Process(
        target=solve_ignore_interrupt,
        args=(queue,),
    )
    solver_process.start()

    time.sleep(1)

    os.kill(solver_process.pid, signal.SIGINT)
    return queue.get()
