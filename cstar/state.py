from contextvars import ContextVar
from typing import List, Optional

from cstar.core import Context

_CONTEXT_STACK: ContextVar[List["Context"]] = ContextVar(
    "active_context_stack", default=[]
)


def get_current_context() -> Optional[Context]:
    stack = _CONTEXT_STACK.get()
    return stack[-1] if stack else None
