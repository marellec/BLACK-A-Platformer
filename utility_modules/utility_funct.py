
import inspect
from typing import Callable





def same_funct_signature(*functs: Callable) -> bool:
    f0 = functs[0]
    for f in functs[1:]:
        
        f_sig = inspect.signature(f)
        
        # for k, val in inspect.signature(f0):
        #     pass
        
        # if (inspect.signature(f) != inspect.signature(f0)):
        #     return False
    return True


def funct_namespace(f: Callable, /) -> str:
    namespace_end = f.__qualname__.find(".")
    if (namespace_end == -1):
        return "main"
    return f.__qualname__[:namespace_end]