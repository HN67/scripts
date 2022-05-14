"""Compute probability distribution of dice rolls.

Especially, the distribution of the sum of independent dice values.
"""

import collections
import collections.abc as c
import itertools
import math
import operator
import string


def parse_roll(command: str) -> c.Iterable[int]:
    """Convert a roll command into an iterable of dice values.

    For example, '2d6 + 3d8' produces (6, 6, 8, 8, 8).

    Not whitespace or case sensitive.
    Expects a sequence of <int>d<int> terms seperated with plus symbols.
    """
    # remove whitespace and cast to lowercase
    # maketrans makes a table that translates the first parameter to the second characterwise
    # and removes any characters in the third parameter
    normal = command.translate(str.maketrans("", "", string.whitespace)).lower()
    # extract the pair of numbers from each roll
    pairs = (group.split("d") for group in normal.split("+"))
    for pair in pairs:
        if len(pair) != 2:
            raise ValueError(f"Invalid roll term, {'d'.join(pair)}")
        # safe to unpack due to previous check
        count, die = pair
        # may raise value error if cannot be cast to int
        yield from itertools.repeat(int(die), int(count))


def probability(dice: c.Iterable[int]) -> c.Mapping[int, float]:
    """Compute the probability of each total when rolling independent dice.

    Probability is a float in the interval [0, 1].
    """
    distr: collections.defaultdict[int, float] = collections.defaultdict(lambda: 0)
    ranges = [range(1, die + 1) for die in dice]
    size = math.prod(len(r) for r in ranges)
    for total in (sum(event) for event in itertools.product(*ranges)):
        # since the product is given ranges it should be capable of computing its length
        distr[total] += 1 / size
    return distr


def display_probability(
    distribution: c.Mapping[int, float],
    *,
    mark: str = ": ",
    precision: int = 4,
    sep: str = "\n",
) -> str:
    """Format a probability distribution in ascending value order.

    Displays probabilities as a fraction,
    using limit_denominator with the provided `denominator`.

    No trailing seperator.
    """
    return sep.join(
        # format the value, the given mark, and then the probability appropriately rounded
        # e.g. 1: 1/6
        f"{value}{mark}{chance:.{precision}f}"
        # sort the distribution items by the value
        for value, chance in sorted(distribution.items(), key=operator.itemgetter(0))
    )
