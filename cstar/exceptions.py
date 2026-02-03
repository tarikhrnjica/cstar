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
class CStarError(Exception):
    """Base class for all C* language errors."""

    pass


class ObstructionError(CStarError):
    """
    Raised when a specific definition violates physical laws.
    Analogue: TypeError, ValueError

    Example:
        Context('Bad', [X, Z])  # Doesn't commute
    """

    pass


class CohomologyError(CStarError):
    """
    Raised when the global topology prevents circuit generation.
    Analogue: LinkerError, RecursionError

    Example:
        The logic contains a paradox.
    """

    pass
