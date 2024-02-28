__all__ = ["Byte", "Integer", "Long", "Double", "String", "List", "Compound"]

class InvalidTypeError(ValueError):
    def __init__(self, item, subtype):
        self.item = item
        self.subtype = subtype
        super().__init__(f"{self.item!r} is not of type {self.subtype.__name__}")

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

class Integer(NumericInteger):
    __slots__ = ()
    size = 4

class Long(NumericInteger):
    __slots__ = ()
    size = 8

class Double(Numeric, float):
    __slots__ = ()

class String(Base, str):
    __slots__ = ()
    
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        self = self.replace(r'\"', '"').replace(r'\\', '\\')
        return self

class List(Base, list):
    __slots__ = ()
    subtype = None
    
    def __new__(cls, iterable=()):
        if cls.subtype is None:
            iterable = tuple(iterable)
            cls.subtype = cls.infer_type(iterable)
        if cls.subtype is not None:
            cls = type(f"{cls.__name__}[{cls.subtype.__name__}]", (cls,), {"__slots__": (), "subtype": cls.subtype})
        return super().__new__(cls, iterable)

    @staticmethod
    def infer_type(iterable):
        subtype = None
        for element in iterable:
            if not issubclass(type(element), Base):
                continue
            if not isinstance(element, Base):
                raise InvalidTypeError(element, Base)
            if subtype is None:
                subtype = type(element)
                continue
            if not isinstance(element, subtype):
                raise InvalidTypeError(element, subtype)
        return subtype
    
    @classmethod
    def cast_item(cls, item):
        if cls.subtype is None:
            raise ValueError("You cannot add items to an empty List without a specified subtype.")
        if not isinstance(item, cls.subtype):
            try:
                return cls.subtype(item)
            except Exception as e:
                raise CastError(item, cls.subtype) from e
            
    
class Compound(dict):
    pass