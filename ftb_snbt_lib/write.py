from contextlib import contextmanager
from .tag import *

__all__ = ["get_writer", "dumps", "dump"]

ESCAPE_SUBS = {
    "\\": "\\\\",
    '"': '\\"'
}

def get_writer():
    """Get the FTB snbt writer object.
    
    Example
    -------
        >>> import ftb_snbt
        >>> writer = ftb_snbt.get_writer()
        >>> snbt = Compound({
        ...     'some_tag': String('some_value'),
        ...     'another_tag': Byte(1)
        ... })
        >>> dumped_snbt = writer.write(snbt)
        >>> print(dumped_snbt)
        {
            some_tag: "some_value"
            another_tag: 1b
        }
    """
    return Writer()

def dumps(tag: Base) -> str:
    """Dump an FTB snbt tag to a string.
    
    A tag can be a ``Compound``, ``List``, ``Numeric``, ``Bool``, or ``String`` object.
    
    The returned string can be written to a file or sent over a network.

    Args
    ----
        tag (Base): The FTB snbt tag to dump.

    Returns
    -------
        str: The dumped FTB snbt string.
        
    Example
    -------
        >>> import ftb_snbt
        >>> snbt = Compound({
        ...     'some_tag': String('some_value'),
        ...     'another_tag': Byte(1)
        ... })
        >>> dumped_snbt = ftb_snbt.dumps(snbt)
        >>> print(dumped_snbt)
        {
            some_tag: "some_value"
            another_tag: 1b
        }
    """
    return get_writer().write(tag) + "\n"

def dump(tag: Base, fp) -> None:
    """Dump an FTB snbt tag to a file.

    Args
    ----
        tag (Base): The FTB snbt tag to dump.
        fp (io.TextIOWrapper): The file to write the FTB snbt tag to (opened in writing text mode with a UTF-8 encoding.)
    
    Example
    -------
        >>> import ftb_snbt
        >>> snbt = Compound({
        ...     'some_tag': String('some_value'),
        ...     'another_tag': Byte(1)
        ... })
        >>> ftb_snbt.dump(snbt, open('some_file.snbt', 'w', encoding='utf-8'))
    """
    fp.write(dumps(tag))

class Writer:
    def __init__(self):
        self.indentation = "\t"
        
        self.indent = ""
        self.prev_indent = ""
        
    @contextmanager
    def depth(self):
        if self.indentation is None:
            yield
        else:
            prev = self.prev_indent
            self.prev_indent = self.indent
            self.indent += self.indentation
            yield
            self.indent = self.prev_indent
            self.prev_indent = prev
            
    def should_expand(self, tag: List | Compound) -> bool:
        return (
            self.indentation is not None
            and (
                not self.prev_indent
                or isinstance(tag, (List, Compound))
            )
        )

    def expand(self, fmt: str) -> tuple[str, str]:
        return (
            f"\n{self.indent}",
            fmt.replace("{}", f"\n{self.indent}{{}}\n{self.prev_indent}"),
        )

    def write(self, tag: Base | str) -> str:
        func = getattr(self, f"write_{tag.write_func}", None)
        return func(tag) if func else f"{tag}"
    
    def write_numeric(self, tag: Numeric) -> str:
        func = int.__repr__ if isinstance(tag, int) else float.__repr__
        return f"{func(tag)}{tag.suffix}"
    
    def write_bool(self, tag: Bool) -> str:
        return "true" if tag else "false"
    
    def write_string(self, tag: String) -> str:
        for match, seq in ESCAPE_SUBS.items():
            tag = tag.replace(match, seq)
        return f'"{tag}"'
    
    def write_list(self, tag: List) -> str:
        separator, fmt = "\n", "[{}]"

        if len(tag) == 0:
            return fmt.format(" ")
        if len(tag) == 1:
            return fmt.format(self.write(tag[0]))
        
        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(fmt)

            return fmt.format(separator.join(map(self.write, tag)))
    
    def write_compound(self, tag: Compound) -> str:
        separator, fmt = "\n", "{{{}}}"

        if len(tag) == 0:
            return fmt.format(" ")
        
        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(fmt)

            return fmt.format(
                separator.join(
                    f"{self.stringify_compound_key(key)}: {self.write(value)}"
                    for key, value in tag.items()
                )
            )
            
    def stringify_compound_key(self, key: String | str) -> str:
        if isinstance(key, String):
            return self.write_string(key)
        return key