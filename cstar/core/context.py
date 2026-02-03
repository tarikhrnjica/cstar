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
from typing import List

import numpy as np

from ..exceptions import ObstructionError
from ..state import _CONTEXT_STACK
from .observable import Observable


class Context:
    """
    A commutative subalgebra of operators.
    Represents a 'Classical Snapshot' or measurement setup.
    """

    def __init__(self, name: str, observables: List[Observable]):
        self.name = name
        self.observables = observables
        self._validate_commutativity()

    def _validate_commutativity(self):
        """
        Enforce the Law of the Subalgebra:
        All operators within a context must commute ([A, B] = 0).
        """
        for i, op_a in enumerate(self.observables):
            for op_b in self.observables[i + 1 :]:
                comm = op_a.matrix @ op_b.matrix - op_b.matrix @ op_a.matrix
                if not np.allclose(comm, 0, atol=1e-9):
                    raise ObstructionError(
                        f"Context '{self.name}' is invalid. "
                        f"'{op_a.name}' and '{op_b.name}' do not commute."
                    )

    def __repr__(self):
        return f"<Context: {self.name}>"

    def __enter__(self):
        # 1. Get the current stack for this thread
        stack = _CONTEXT_STACK.get()

        # 2. Vital: If this is the first context in this thread,
        # 'default=[]' shares the SAME list object across threads if we aren't careful.
        # We must ensure we have a unique list for this context execution.
        if stack == []:
            # If it's the default empty list, make a new one so we don't mutate the default
            stack = []

        # 3. Push self
        stack.append(self)

        # 4. Update the context var (mostly for safety if we replaced the list object)
        self._token = _CONTEXT_STACK.set(stack)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 1. Get current stack
        stack = _CONTEXT_STACK.get()

        # 2. Pop self
        stack.pop()

        # 3. No need to reset token if we mutated the list in place,
        # but resetting is cleaner if we want strictly scoped behavior.
        # Ideally, we just leave the list mutated.
