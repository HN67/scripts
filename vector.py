"""Implementation of mathematical Vector"""

import typing

class Vector:
    """Attempts to simulate a general mathematical numerical (Euclidean?) vector\n
    Can be constructed with a single iterable or multiple values\n
    Changing the dimension (length) after creation of a vector should be avoided probably
    """

    def __init__(self, *components: float):

        # Single parameter
        if len(components) == 1:
            # Ensures that that provided argument is iterable and transforms to a tuple
            self.components = tuple(components[0])

        # Multiple parameters
        else:
            # Reference the provided parameters (* notation provides a tuple already)
            self.components = components

        # Determine dimension
        self.dimension = len(self.components)

    def __str__(self):
        """Returns the printable string representation of the Vector"""
        return f"{type(self).__name__}{self.components}"

    def __len__(self):
        """Returns the dimension as the length"""
        return self.dimension

    def __getitem__(self, index):
        """Returns the item of the components, also allows iteration"""
        if 0 <= index < self.dimension:
            return self.components[index]
        # Not within valid range of indexes
        raise IndexError(f"Expected index between 0 and {self.dimension}")

    def __add__(self, other: typing.Iterable):
        """Adds to another vector or iterable of equal dimension"""
        # Adds each component independtly into a new Vector
        if len(self) == len(other):
            return type(self)(left + right for left, right in zip(self, other))
        raise ValueError(f"Mismatched lengths of {self}<{len(self)}> and {other}<{len(other)}>")

    def __radd__(self, other: typing.Iterable):
        return self.__add__(other)

    def __sub__(self, other: typing.Iterable):
        """Subtracts another vector or iterable of equal dimension from this one"""
        # Subtracts each component independtly into a new Vector
        if len(self) == len(other):
            return type(self)(left - right for left, right in zip(self, other))
        raise ValueError(f"Mismatched lengths of {self}<{len(self)}> and {other}<{len(other)}>")

    def __rsub__(self, other: typing.Iterable):
        """Subtracts this vector from another vector or iterable of equal dimension"""
        # Due to the noncommutivity of subtraction,
        # this method must be maintained independently of sub dunder
        if len(self) == len(other):
            # Key difference currently is in <right, left> instead of <left, right>
            return type(self)(left - right for right, left in zip(self, other))
        raise ValueError(f"Mismatched lengths of {self}<{len(self)}> and {other}<{len(other)}>")

    def __mul__(self, other: float):
        """Multiplies the vector (each component) by a scalar"""
        return type(self)(component * other for component in self.components)

    def __rmul__(self, other: float):
        return self.__mul__(other)

    def __neg__(self):
        """Returns a vector with negatively inverted components"""
        return type(self)(-component for component in self.components)
