import datetime
from zteb.crypto import TimeLockPuzzle
from zteb.crypto.symmetric import generate_key, SymmetricEncryptionScheme
from .conftest import start_solving_and_interrupt


def test_symmetric_encryption(message: str):
    key = generate_key()
    scheme = SymmetricEncryptionScheme(key)

    cypher = scheme.encrypt(message)
    assert cypher != message

    decrypted = scheme.decrypt(cypher)
    assert decrypted == message


def test_time_lock_puzzle(
        message: str,
        puzzle: TimeLockPuzzle,
        puzzle_duration: datetime.timedelta
):
    """
    The puzzle should be correctly solvable in
    more than half and less than double the desired duration.
    """
    # instructions are always accessible
    assert puzzle.instructions is not None

    start = datetime.datetime.now()
    puzzle.solve()
    end = datetime.datetime.now()
    time_elapsed = end - start

    assert puzzle.is_solved

    assert time_elapsed > puzzle_duration/2
    assert time_elapsed < puzzle_duration*2

    assert puzzle.solution == message


def test_time_lock_puzzle_interruption(message: str, puzzle: TimeLockPuzzle):
    """
    The puzzle should automatically save its state on interruption.
    It should be possible to continue solving the puzzle later.
    """
    total_iterations = puzzle.remaining_iterations

    puzzle = start_solving_and_interrupt(puzzle)

    assert not puzzle.is_solved
    assert puzzle.remaining_iterations < total_iterations

    puzzle.solve()

    assert puzzle.is_solved
    assert puzzle.solution == message


def test_time_lock_puzzle_serialization(message: str, puzzle: TimeLockPuzzle):
    dump = puzzle.dump()
    loaded_puzzle = puzzle.load(dump)
    loaded_puzzle.solve()

    assert loaded_puzzle.is_solved
    assert loaded_puzzle.solution == message


def test_time_lock_puzzle_deserialization_after_interrupt(
        message: str,
        puzzle: TimeLockPuzzle
):
    puzzle = start_solving_and_interrupt(puzzle)

    assert not puzzle.is_solved

    dump = puzzle.dump()
    loaded_puzzle = puzzle.load(dump)
    loaded_puzzle.solve()

    assert loaded_puzzle.is_solved
    assert loaded_puzzle.solution == message
