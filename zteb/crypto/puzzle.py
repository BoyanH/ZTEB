"""
Time-lock-puzzles related functionality.
"""


import datetime
import random
import pickle
from dataclasses import dataclass
from tqdm import tqdm
from zteb.exceptions import PuzzleNotSolvedException
from .primes import get_large_primes_tuple
from .symmetric import generate_key, SymmetricEncryptionScheme


_FIVE_SECONDS = datetime.timedelta(seconds=5)


@dataclass
class TimeLockPuzzle:
    """
    See http://people.csail.mit.edu/rivest/RivestShamirWagner-timelock.pdf
    """
    # pylint: disable=too-many-instance-attributes
    # This is after all an implementation of a weird cryptographic algorithm.
    # And it's for fun anyways...

    # as in paper
    _n: int
    _a: int
    _t: int
    _c_k: int
    _c_m: bytes

    # additional
    _key_length: int
    _instructions: str = None
    _solution: str = None

    # inferred
    _total_iterations: int = None

    def __post_init__(self):
        # when total iterations aren't set, then the puzzle was just generated
        if not self._total_iterations:
            self._total_iterations = self._t

    @property
    def instructions(self):
        return self._instructions

    @property
    def solution(self):
        """
        Returns
        -------
        The solution of the puzzle, as passed on puzzle creation.

        Raises
        ------
        PuzzleNotSolvedException
            If the puzzle hasn't been solved yet.
        """
        if self._solution:
            return self._solution

        raise PuzzleNotSolvedException

    @property
    def is_solved(self) -> bool:
        return self._solution is not None

    @property
    def remaining_iterations(self) -> int:
        return self._t

    @property
    def total_iterations(self) -> int:
        return self._total_iterations

    def solve(self, show_progress=False):
        """
        Solves the puzzle.
        Its message can be accessed with `puzzle.message` afterwards.
        """
        b = self._compute_b(show_progress)

        # decrypt and return
        key_int = (self._c_k - b) % self._n
        key = int.to_bytes(key_int, self._key_length, byteorder='big')
        scheme = SymmetricEncryptionScheme(key)

        self._solution = scheme.decrypt(self._c_m)

    def _compute_b(self, show_progress: bool) -> int:
        # using local variables should speed this up significantly
        n = self._n
        # a and t really need to be updated atomically
        at = (self._a, self._t)
        try:
            iterator = tqdm(
                range(at[1]),
                initial=self.total_iterations - self.remaining_iterations,
                total=self.total_iterations,
                disable=not show_progress,
            )
            for _ in iterator:
                at = (pow(at[0], 2, n), at[1] - 1)

            return at[0]
        finally:
            # store state, no matter whether interrupted or not...
            self._a, self._t = at

    def dump(self) -> bytes:
        """
        Dumps a TimeLockPuzzle in binary format.
        """
        representation = self.__dict__
        return pickle.dumps(representation)

    @classmethod
    def load(cls, state: bytes) -> 'TimeLockPuzzle':
        """
        Loads a TimeLockPuzzle from binary dump.
        """
        representation = pickle.loads(state)
        return cls(**representation)

    @classmethod
    def generate(
            cls,
            solution: str,
            instructions: str = '',
            desired_duration: datetime.timedelta = _FIVE_SECONDS,
    ) -> 'TimeLockPuzzle':
        """
        Parameters
        ----------
        solution
            Can be retrieved after solving the puzzle
        instructions
            Optional information which can be accessed
             before solving the puzzle
        desired_duration
            The amount of time it should optimally take to solve the puzzle
        Returns
        -------
        A new puzzle time lock puzzle with the desired properties.
        """
        # pylint: disable=too-many-locals
        # yes, it gets numerical and variable-rich

        # classic encryption
        key = generate_key()
        scheme = SymmetricEncryptionScheme(key)
        message_cypher = scheme.encrypt(solution)

        # generate challenge
        p, q = get_large_primes_tuple()
        n = p * q
        phi = (p - 1) * (q - 1)
        a = random.randint(2, n - 1)

        mean_iterations_per_second = cls._get_iterations_per_second(n, phi)
        iterations = mean_iterations_per_second * int(desired_duration.total_seconds())

        e = pow(2, iterations, phi)
        b = pow(a, e, n)
        key_int = int.from_bytes(key, byteorder='big')
        key_cyper = (key_int + b) % n

        return cls(
            _n=n,
            _a=a,
            _t=iterations,
            _c_k=key_cyper,
            _c_m=message_cypher,
            _key_length=len(key),
            _instructions=instructions,
        )

    @classmethod
    def _get_iterations_per_second(
            cls,
            a: int,
            n: int,
            trials=int(1e5)
    ) -> int:
        start = datetime.datetime.now()
        for _ in range(trials):
            a = pow(a, 2, n)
        end = datetime.datetime.now()

        time_elapsed = end - start
        return trials // time_elapsed.seconds
