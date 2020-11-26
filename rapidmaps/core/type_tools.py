from typing import Any


def same_type(base_val: Any, check_val: Any) -> bool:
    return True if base_val is not None and \
                   check_val is not None and \
                   isinstance(check_val, type(base_val)) else False
