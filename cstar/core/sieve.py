#
# Copyright (c) 2026-present Tarik Hrnjica <tarik.hrnjica@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import numpy as np

from cstar.core import Context


class Sieve:
    def __init__(
        self, projector: np.ndarray, context: Context = None, is_undefined: bool = False
    ):
        self.projector = projector
        self.context = context
        self._is_undefined = is_undefined

    @classmethod
    def Undefined(cls, dim: int, context: Context = None):
        """
        Represents a logical category error.
        Example: Asking for Position inside a Momentum context.
        """
        return cls(np.zeros((dim, dim)), context, is_undefined=True)

    @classmethod
    def Min(cls, dim: int, context: Context = None):
        """False / Bottom"""
        return cls(np.zeros((dim, dim)), context)

    @classmethod
    def Max(cls, dim: int, context: Context = None):
        """True / Top"""
        return cls(np.eye(dim), context)

    def __repr__(self):
        if self._is_undefined:
            return "<Sieve: Undefined>"

        dim_trace = np.trace(self.projector).real
        dims = self.projector.shape[0]
        if np.isclose(dim_trace, dims):
            return "<Sieve: Max>"
        if np.isclose(dim_trace, 0):
            return "<Sieve: Min>"

        return f"<Sieve: dim={dim_trace:.1f} in {self.context.name}>"

    def __invert__(self):
        if self._is_undefined:
            return self

        id = np.eye(self.projector.shape[0])
        return Sieve(id - self.projector, self.context)

    def __and__(self, other: "Sieve"):
        if self._is_undefined or other._is_undefined:
            return Sieve.Undefined(self.projector.shape[0], self.context)

        return Sieve(self.projector @ other.projector, self.context)

    def __or__(self, other: "Sieve"):
        if self._is_undefined or other._is_undefined:
            return Sieve.Undefined(self.projector.shape[0], self.context)

        p, q = self.projector, other.projector
        return Sieve(p + q - p @ q, self.context)
