from contextlib import contextmanager
from .tag import *

__all__ = ["get_writer", "dumps", "dump"]

ESCAPE_SUBS = {
    "\\": "\\\\",
    '"': '\\"'
}

class Writer:
    def __init__(self, comma_sep: bool = False):
        self.indentation = "\t"
        self.indent = ""
        self.prev_indent = ""
        
        self.separator = "\n"
        if comma_sep:
            self.separator = "," + self.separator
        
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
            
    def should_expand(self, tag: List | Array | Compound) -> bool:
        return (
            self.indentation is not None
            and (
                not self.prev_indent
                or isinstance(tag, (List, Array, Compound))
            )
        )

    def expand(self, separator: str, fmt: str) -> tuple[str, str]:
        return (
            f"{separator}{self.indent}",
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
        separator, fmt = self.separator, "[{}]"

        if len(tag) == 0:
            return fmt.format(" ")
        if len(tag) == 1:
            return fmt.format(self.write(tag[0]))
        
        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(separator, fmt)

            return fmt.format(separator.join(map(self.write, tag)))
        
    def write_array(self, tag: Array) -> str:
        separator, fmt = self.separator, f"[{tag.array_prefix};{{}}]"

        if len(tag) == 0:
            return fmt.format(" ")
        if len(tag) == 1:
            return fmt.format(self.write(tag[0]))
        
        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(separator, fmt)

            return fmt.format(separator.join(map(self.write, tag)))
    
    def write_compound(self, tag: Compound) -> str:
        separator, fmt = self.separator, "{{{}}}"

        if len(tag) == 0:
            return fmt.format(" ")
        
        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(separator, fmt)

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
    
def get_writer(comma_sep: bool = False) -> Writer:
    """Get the FTB snbt writer object.
    
    Args
    ----
        comma_sep (bool): Whether to separate tags with commas.
        
    Returns
    -------
        Writer: The FTB snbt writer object.
    
    Example
    -------
        >>> import ftb_snbt_lib as slib
        >>> writer = slib.get_writer()
        >>> snbt = slib.Compound({
        ...     'some_tag': slib.String('some_value'),
        ...     'another_tag': slib.Byte(1)
        ... })
        >>> dumped_snbt = writer.write(snbt)
        >>> print(dumped_snbt)
        {
            some_tag: "some_value"
            another_tag: 1b
        }
    """
    return Writer(comma_sep=comma_sep)

def dumps(tag: Base, comma_sep: bool = False) -> str:
    """Dump an FTB snbt tag to a string.
    
    A tag can be a ``Compound``, ``List``, ``Numeric``, ``Bool``, or ``String`` object.
    
    The returned string can be written to a file or sent over a network.

    Args
    ----
        tag (Base): The FTB snbt tag to dump.
        comma_sep (bool): Whether to separate tags with commas.

    Returns
    -------
        str: The dumped FTB snbt string.
        
    Example
    -------
        >>> import ftb_snbt_lib as slib
        >>> snbt = slib.Compound({
        ...     'some_tag': slib.String('some_value'),
        ...     'another_tag': slib.Byte(1)
        ... })
        >>> dumped_snbt = slib.dumps(snbt)
        >>> print(dumped_snbt)
        {
            some_tag: "some_value"
            another_tag: 1b
        }
    """
    return get_writer(comma_sep=comma_sep).write(tag) + "\n"

def dump(tag: Base, fp, comma_sep: bool = False) -> None:
    """Dump an FTB snbt tag to a file.

    Args
    ----
        tag (Base): The FTB snbt tag to dump.
        fp (io.TextIOWrapper): The file to write the FTB snbt tag to (opened in writing text mode with a UTF-8 encoding.)
        comma_sep (bool): Whether to separate tags with commas.
    
    Example
    -------
        >>> import ftb_snbt_lib as slib
        >>> snbt = slib.Compound({
        ...     'some_tag': slib.String('some_value'),
        ...     'another_tag': slib.Byte(1)
        ... })
        >>> slib.dump(snbt, open('some_file.snbt', 'w', encoding='utf-8'))
    """
    fp.write(dumps(tag, comma_sep=comma_sep))