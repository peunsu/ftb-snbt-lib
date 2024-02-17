__all__ = ["Byte", "Integer", "Long", "Double", "String", "Array", "Compound"]

class Byte(int):
    def __new__(cls, value):
        value = int(value)
        if value < -128 or value > 127:
            raise ValueError(f"Byte value {value} is out of range")
        return super().__new__(cls, value)
    def __repr__(self):
        return f"{int(self)}b"

class Integer(int):
    def __new__(cls, value):
        value = int(value)
        if value < -2147483648 or value > 2147483647:
            raise ValueError(f"Integer value {value} is out of range")
        return super().__new__(cls, value)
    def __repr__(self):
        return f"{int(self)}"

class Long(int):
    def __new__(cls, value):
        value = int(value)
        if value < -9223372036854775808 or value > 9223372036854775807:
            raise ValueError(f"Long value {value} is out of range")
        return super().__new__(cls, value)
    def __repr__(self):
        return f"{int(self)}L"

class Double(float):
    def __new__(cls, value):
        value = float(value)
        if value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308:
            raise ValueError(f"Double value {value} is out of range")
        return super().__new__(cls, value)
    def __repr__(self):
        return f"{float(self)}d"

class String(str):
    def __new__(cls, value = None):
        value = value.replace(r'\"', '"').replace(r'\\', '\\')
        return super().__new__(cls, value)
    def __repr__(self):
        return f'"{str(self)}"'

class Array(list):
    def __new__(cls, value = None):
        return super().__new__(cls, value)
    def __repr__(self):
        return f"[{', '.join(map(repr, self))}]"
    
class Compound(dict):
    def __new__(cls, value = None):
        return super().__new__(cls, value)
    def __repr__(self):
        return f"{{{', '.join(f'{repr(k)}: {repr(v)}' for k, v in self.items())}}}"