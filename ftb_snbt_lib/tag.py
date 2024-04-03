__all__ = ["Base", "Numeric", "NumericInteger", "Byte", "Short", "Integer", "Long", "Double", "Bool", "String", "List", "Compound"]

class InvalidTypeError(ValueError):
    def __init__(self, item, cls):
        self.item = item
        self.cls = cls
        super().__init__(f"{self.item!r} is not a valid type for the items of {cls.__name__}.\nThis error is likely caused by a type mismatch in a list.")

class CastError(ValueError):
    def __init__(self, item, subtype):
        self.item = item
        self.subtype = subtype
        super().__init__(f"{self.item!r} cannot be casted to {self.subtype.__name__}")

class Base:
    __slots__ = ()
    
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)
    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

class Numeric(Base):
    __slots__ = ()
    write_func = "numeric"
    suffix = ""

class NumericInteger(Numeric, int):
    __slots__ = ()
    
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        limit = 2 ** (8 * cls.size - 1)
        cls.range = range(-limit, limit)
    
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        if int(self) not in cls.range:
            raise ValueError(f"{cls.__name__} value {int(self)} is out of range")
        return self

class Byte(NumericInteger):
    __slots__ = ()
    size = 1
    suffix = "b"

class Short(NumericInteger):
    __slots__ = ()
    size = 2
    suffix = "s"

class Integer(NumericInteger):
    __slots__ = ()
    size = 4

class Long(NumericInteger):
    __slots__ = ()
    size = 8
    suffix = "L"

class Double(Numeric, float):
    __slots__ = ()
    suffix = "d"

class Bool(Base, int):
    __slots__ = ()
    write_func = "bool"
    
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        return self

class String(Base, str):
    __slots__ = ()
    write_func = "string"
    
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        return self

class List(Base, list):
    __slots__ = ()
    write_func = "list"
    subtype = None
    
    def __new__(cls, iterable=()):
        if cls.subtype is None:
            iterable = tuple(iterable)
            subtype = cls.infer_type(iterable)
            cls = cls[subtype]
        return super().__new__(cls, iterable)
    
    def __init__(self, iterable=()):
        super().__init__(map(self.cast_item, iterable))
    
    def __class_getitem__(cls, subtype):
        if subtype is None:
            return List
        return type(f"{cls.__name__}[{subtype.__name__}]", (List,), {"__slots__": (), "subtype": subtype})

    @staticmethod
    def infer_type(iterable):
        subtype = None
        
        for item in iterable:
            itemtype = type(item)
            if not issubclass(itemtype, Base):
                continue

            if subtype is None:
                subtype = itemtype
                if not issubclass(subtype, List):
                    return subtype
            elif subtype is not itemtype:
                sub_t, item_t = subtype, itemtype
                while issubclass(sub_t, List) and issubclass(item_t, List):
                    sub_t, item_t = sub_t.subtype, item_t.subtype

                if sub_t is None:
                    subtype = itemtype
                elif item_t is not None:
                    return None
            
        return subtype
    
    def __setitem__(self, index, value):
        if isinstance(index, int):
            super().__setitem__(index, self.cast_item(value))
        elif isinstance(index, slice):
            super().__setitem__(index, map(self.cast_item, value))
        else:
            raise TypeError(f"List indices must be integers or slices, not {index.__class__.__name__}")
        
    def append(self, value):
        super().append(self.cast_item(value))
    
    def extend(self, iterable):
        super().extend(map(self.cast_item, iterable))
    
    def insert(self, index, value):
        super().insert(index, self.cast_item(value))
    
    @classmethod
    def cast_item(cls, item):
        if cls.subtype is None:
            raise InvalidTypeError(item, cls)
        
        if not isinstance(item, cls.subtype):
            try:
                return cls.subtype(item)
            except Exception as e:
                raise CastError(item, cls.subtype) from e
            
        return item
    
class Compound(Base, dict):
    __slots__ = ()
    write_func = "compound"