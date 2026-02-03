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
from cstar import ObstructionError, _get_current_context
from cstar.core import Observable, Sieve


class System:
    def __init__(self, n_qubits: int):
        self.dim = 2**n_qubits

    def measure(self) -> Observable:
        """
        Returns a placeholder observable representing the
        active measurement in the current context.
        """
        ctx = _get_current_context()
        if not ctx:
            raise ObstructionError("Cannot measure outside a Context.")
        return ctx.observables[0]

    @property
    def Min(self):
        """The Minimal Truth for this system."""
        return Sieve.Min(self.dim)

    @property
    def Max(self):
        """The Maximal Truth for this system."""
        return Sieve.Max(self.dim)
