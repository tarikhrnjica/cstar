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
from contextvars import ContextVar
from typing import List, Optional

from .core import Context

_CONTEXT_STACK: ContextVar[List["Context"]] = ContextVar(
    "active_context_stack", default=[]
)


def get_current_context() -> Optional[Context]:
    stack = _CONTEXT_STACK.get()
    return stack[-1] if stack else None
