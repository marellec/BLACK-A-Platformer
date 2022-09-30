

# Entity uses Folder as metaclass
# TileMapForm uses Folder as metaclass
# AnimationPack uses Folder as metaclass

from typing import Callable


# print("\n")


class Folder(type):
    """Folder verifies required Folder attrs and methods:

        -   folder_name (str)
        -   folder_item_name (str)
        -   folder_key (str or type)
        -   folder_value (str or type)
        
        -   __getitem__() method
        -   -   exactly 1 arg with type hint: folder_key

        -    method with name = "add_" + folder_name - "s"
        -   -    exactly 1 arg with type hint: folder_value OR
        -   -    exactly 2 args with type hints: folder_key, folder_value

        -    method with name = "remove_" + folder_name - "s"
        -   -    exactly 1 arg with type hint: folder_key
            
        -    can decorate methods with
        -    -    @abstract_Folder_method OR
        -    -    @special_implementation"""
    
    def __new__(self, class_name, bases, attrs):
        
        # check if all required attributes and methods are in class
        # and check if type hint/annotations are valid
        
        # if tests fail, 
        #   raise AttributeError
        # if all tests pass,
        #   tag class with __metaclass__ for type checking
        
        
        start_error_msg = f"Folder class '{class_name}' has issues:"
        error_msg = start_error_msg
        
        folder_name = None
        item_name = None
        add_method = None
        remove_method = None
        __getitem__method = None
        
        # alert about missing attrs, if any
        
        no_attribute = lambda e: f"\n    missing attribute {str(e)}"
        no_method    = lambda e: f"\n    missing method    {str(e)}"
        
        try:                    folder_name = attrs["folder_name"]
        except KeyError as e:   error_msg += no_attribute(e)
        
        try:                    item_name = attrs["folder_item_name"]
        except KeyError as e:   item_name = folder_name[:-1] if (folder_name is not None) else ""
        
        try:                    __getitem__method = attrs["__getitem__"]
        except KeyError as e:   error_msg += no_method(e)
        
        if (folder_name is None):    # needs folder_name to find other errors
            raise AttributeError(error_msg)
        
        try:                    add_method = attrs[f"add_{item_name}"]
        except KeyError as e:   error_msg += no_method(e)
        
        try:                    remove_method = attrs[f"remove_{item_name}"]
        except KeyError as e:   error_msg += no_method(e)
        
        
        # alert about wrong type hints, if any
        
        
        folder_annotation = None
        
        has_folder_annotations = True
        
        try: 
            folder_annotation = attrs["__annotations__"][folder_name]
        except KeyError as e:   
            error_msg += f"\n    folder attribute '{folder_name}' missing type hints"
            has_folder_annotations = False
        
        if (has_folder_annotations):
            
            # folder must be a dictionary
            if ("dict" in str(folder_annotation)):
                
                try: _ = folder_annotation.__args__ 
                except AttributeError as e: # no key and value type hints
                    error_msg += f"\n    folder attribute '{folder_name}' missing [key, val] type hints"
                    has_folder_annotations = False
            else:
                error_msg += f"\n    folder attribute '{folder_name}' is not a dictionary"
                has_folder_annotations = False
        
        
        if (not has_folder_annotations): # needs type hints to find other errors
            raise AttributeError(error_msg)
        
        folder_key = folder_annotation.__args__[0]
        folder_value = folder_annotation.__args__[1]
        
        folder_key_name   = folder_key.__qualname__
        folder_value_name = folder_value.__qualname__
        
        # convert type to a str, whether it is a str, or a type
        convert_type_str = lambda s : (s if (type(s) == str) else s.__qualname__)    
        
        # ADD METHOD
        
        if (add_method is not None):
            
            special_add = True
                
            try: 
                _ = attrs[add_method.__name__].__special_Folder_method__
            except AttributeError:
                special_add = False
                
            if (not special_add):
                
                ann_num = len(add_method.__annotations__)
                arg_num = add_method.__code__.co_argcount - 1
                missing_ann_num = arg_num - ann_num
                
                if (ann_num == 0):
                    error_msg += f"\n    {add_method.__name__}() missing type hints"
                if (arg_num > 2):
                    error_msg += f"\n    {add_method.__name__}() has {arg_num} args, should be <= 2"
                
                if (ann_num < arg_num):
                    error_msg += (f"\n    {add_method.__name__}() has {missing_ann_num} arg" + 
                                  ("s" if (missing_ann_num > 1) else "") + 
                                   " without type hints")
                
                
                for i, (arg, hint) in enumerate(add_method.__annotations__.items()):
                    
                    hint = convert_type_str(hint)
                    
                    if (ann_num == 1): # add using value only
                        if (hint != folder_value_name):
                            error_msg += (f"\n    {add_method.__name__}() arg '{arg}' has "
                                          f"hint '{hint}', should be '{folder_value_name}'")
                    else:             # add using key and value
                        if   (i == 0 and
                            hint != folder_key_name):
                            error_msg += (f"\n    {add_method.__name__}() arg 1 '{arg}' has "
                                          f"hint '{hint}', should be '{folder_key_name}'")
                        elif (i == 1 and
                            hint != folder_value_name):
                            error_msg += (f"\n    {add_method.__name__}() arg 2 '{arg}' has "
                                          f"hint '{hint}', should be '{folder_value_name}'")
        
        
        # REMOVE METHOD and ACCESS METHOD
        
        special_remove = True
                
        try: 
            _ = attrs[remove_method.__name__].__special_Folder_method__
        except AttributeError:
            special_remove = False
            
        special__getitem__ = True
                
        try: 
            _ = attrs[__getitem__method.__name__].__special_Folder_method__
        except AttributeError:
            special__getitem__ = False
            
        
        for method in (None if (special_remove) else remove_method, 
                       None if (special__getitem__) else __getitem__method):
            
            if (method is None):
                continue
            
            if (method == __getitem__method):
            
                return_hint = None
                
                if ("return" in method.__annotations__):
                    return_hint = convert_type_str(method.__annotations__["return"])
                    del method.__annotations__["return"]
                    
                    if (return_hint != folder_value_name):
                        error_msg += (f"\n    __getitem__() has return type "
                                      f"hint '{return_hint}', should be '{folder_value_name}'")
                else:
                    error_msg += f"\n    __getitem__() missing return type hint '{folder_value_name}'"
            
            ann_num = len(method.__annotations__)
            arg_num = method.__code__.co_argcount - 1
            missing_ann_num = arg_num - ann_num
        
            if (ann_num == 0):
                error_msg += f"\n    {method.__name__}() missing type hints"
            if (arg_num > 1):
                error_msg += f"\n    {method.__name__}() has {arg_num} args, should be 1"
        
            if (ann_num < arg_num):
                error_msg += (f"\n    {method.__name__}() has {missing_ann_num} arg" + 
                               ("s" if (missing_ann_num > 1) else "") + 
                                " without type hints")

            
            for arg, hint in method.__annotations__.items():
                
                hint = convert_type_str(hint)
                
                if (hint != folder_key_name):
                    error_msg += (f"\n    {method.__name__}() arg '{arg}' has "
                                  f"hint '{hint}', should be '{folder_key_name}'")
        
        
        if (error_msg == start_error_msg): # no errors, automatically set methods
            
            abstract_remove = True
            
            try: 
                attrs[remove_method.__name__].__abstract_Folder_method__
                
            except AttributeError:
                abstract_remove = False
            
            if (abstract_remove):
                
                def temp_name(self, key: folder_key):
                    del self.__dict__[folder_name][key]
                    return self
                
                temp_name.__name__ = remove_method.__name__ # rename method
                
                attrs[remove_method.__name__] = temp_name
            
            
            
            abstract__getitem__ = True
                
            try: 
                _ = attrs["__getitem__"].__abstract_Folder_method__
            except AttributeError:
                abstract__getitem__ = False
                
            if (abstract__getitem__):
                
                def __getitem__(self, key: folder_key) -> folder_value:
                    try:
                        return self.__dict__[folder_name][key]
                    except KeyError:
                        raise KeyError(f"No {item_name} of type '" + f"{str(key)}" +
                                        # (key.name if (folder_key_name == "Label") # type: ignore
                                        # else f"{str(key)}") +
                                       f"' was found in {folder_name}")
                
                attrs["__getitem__"] = __getitem__
                
            if (not abstract__getitem__ and # __getitem__() should be auto-created or
                not special__getitem__):    # be tagged special
                error_msg += ("\n    __getitem__() is not tagged"
                              "\n\t@abstract_Folder_method OR"
                              "\n\t@special_implementation")
                raise AttributeError(error_msg)
            
            
        else: # alert all errors in one message
            raise AttributeError(error_msg)
        
        
        # tag class with __metaclass__ for type checking
        attrs['__metaclass__'] = Folder
        
        
        return type(class_name, bases, attrs)
    

# returns True if given object is a class with Folder as metaclass OR
# object is of a type that has Folder as its metaclass
def is_folder(obj):
    
    if (type(obj) == type):
        try:
            return obj.__metaclass__ == Folder
        except AttributeError:
            return False
    else:
        try:
            return obj.__class__.__metaclass__ == Folder
        except AttributeError:
            return False
        


def abstract_Folder_method(method: Callable):
    """METHOD decorator that tags abstract Folder methods
    \nthe body of these methods will be AUTO-filled
    \nno method can be abstract AND special
    \nadd_item() method CANNOT be abstract
    \n__getitem__() must be tagged abstract OR special"""
    method.__abstract_Folder_method__ = True # type: ignore
    return method


def special_implementation(method: Callable):
    """METHOD decorator that tags Folder methods with unique signatures
    \nthese methods' signatures will NOT be checked for validity
    \nno method can be special AND abstract
    \n__getitem__() must be tagged abstract OR special"""
    method.__special_Folder_method__ = True # type: ignore
    return method



# class Entity(metaclass=Folder):
    
#     folder_name = "traits"
    
#     traits:  dict[str, int]
    
#     def __init__(self):
#         self.traits = {}
    
#     def add_trait(self, trait: int):
#         self.traits[str(trait)] = trait
#         return self
    
#     @abstract_Folder_method
#     def remove_trait(self, trait_label: str):
#         pass
        
#     @special_implementation
#     def __getitem__(self, trait_label: str) -> int:
#         pass
    
    

    
    




# e = Entity()

# (
#     e.add_trait(3)
#      .add_trait(4)
#      .add_trait(5)
# )

# print(is_folder(e))
# print(is_folder(Entity))

# e.remove_trait("5")

# print(e)
# print(e.traits)
# print(e["4"])



# print("\n")