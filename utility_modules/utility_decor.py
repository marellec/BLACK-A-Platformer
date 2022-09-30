
from dataclasses import dataclass
import inspect
from typing import Callable


# 1 class, some functions, and some decorators 
# for semi-abstract non-implmented methods


# CLASS vvv

# container to tag and render unusable non-implemented methods
@dataclass
class NotImplemented:
    method: Callable
    
    def __call__(self, *args, **kwds):
        self.method(*args, **kwds) # will raise the NotImplementedError specified in parent class


# FUNCTIONS vvv

# checks if method is implemented
def is_implemented(parent_class: type, method: Callable) -> bool:
    return (type(method).__name__ == "method" and # has been implemented as a function
            type(parent_class.__dict__[method.__name__]).__name__ == "NotImplemented") # was tagged non-implemented in parent class



# DECORATORS vvv

# METHOD decorator to tag a non-implemented method as a NotImplemented
def not_implemented(method: Callable, /):
    return NotImplemented(method)

# CLASS decorator that validates all implemented methods in the decorated class
# based off non-implemented outlines of those methods in given parent class
def has_implemented(parent_class: type, **methods: bool):
    
    def validator(child_class: type) -> type:
        start_error_msg = f"{child_class.__name__} has method implementation issues:"
        error_msg = start_error_msg
        
        if (issubclass(child_class, parent_class)): # child_class is a child of parent_class
            
            for method_name, val in methods.items():
                
                parent_method = parent_class.__dict__[method_name]
                
                method_funct = child_class.__dict__[method_name]
                
                if (val): # implemented method
                    
                    if (isinstance(parent_method, NotImplemented)): # was correctly tagged
                        
                        parent_method_funct = parent_method.method # get function from NotImplemented obj
                        
                        # convert type to a str, whether it is a str, or a type
                        convert_type_str = lambda s : (s if (type(s) == str) else s.__qualname__)    
                        
                        # different signatures
                        
                        parent_arg_num = parent_method_funct.__code__.co_argcount - 1
                        
                        ann_num = len(method_funct.__annotations__)
                        arg_num = method_funct.__code__.co_argcount - 1
                        missing_ann_num = arg_num - ann_num
                        
                        if (ann_num == 0):
                            error_msg += f"\n    {method_name}() missing type hints"
                        if (arg_num != parent_arg_num):
                            error_msg += f"\n    {method_name}() has {arg_num} args, should be {parent_arg_num}"
                        
                        if (ann_num < arg_num):
                            error_msg += (f"\n    {method_name}() has {missing_ann_num} arg" + 
                                          ("s" if (missing_ann_num > 1) else "") + 
                                           " without type hints")
                        
                        for arg, parent_hint in parent_method_funct.__annotations__.items():
                    
                            parent_hint = convert_type_str(parent_hint)
                            
                            method_hint = ""
                            
                            try:             method_hint = method_funct.__annotations__[arg]
                            except KeyError: error_msg += f"\n    {method_name}() arg '{arg}' missing type hint '{parent_hint}'"
                            
                            if (method_hint != "" and
                                convert_type_str(method_hint) != parent_hint):
                                error_msg += f"\n    {method_name}() arg '{arg}' should have type hint '{parent_hint}'"
                                
                            
                        if (error_msg == start_error_msg): # no errors so far
                            
                            for parent_arg, method_arg in zip(parent_method_funct.__annotations__,
                                                              method_funct.__annotations__):
                                if (method_arg != parent_arg):
                                    error_msg += f"\n    {method_name}() has arg '{method_arg}' where '{parent_arg}' should be"
                        
                    else: # was NOT tagged non-implemented in parent class
                        error_msg += (f"\n    method '{method_name}' wasn't tagged @not_implemented "
                                      f"in parent class {parent_class.__name__}")
                
            if (error_msg != start_error_msg): # raise error if any
                raise NotImplementedError(error_msg)
        else:  # child_class is NOT a child of parent_class
            error_msg += f"\n    {child_class.__name__} does not inherit from {parent_class.__name__}"
            raise NotImplementedError(error_msg)
    
        return child_class
    
    return validator
            
            

# print("\n")


# class BParent:
    
#     def __init__(self):
#         pass
    
#     @not_implemented
#     def hi(self, a: str):
#         pass

# @has_implemented(BParent, hi=True)
# class Bh(BParent):
    
#     def __init__(self):
#         pass
    
#     def hi(self, b: str):
#         print("hello")


# print("\n")