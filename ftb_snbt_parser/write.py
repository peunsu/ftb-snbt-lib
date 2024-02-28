import re
from contextlib import contextmanager
from .tag import *

STRING_QUOTES = {
    '"': "'",
    "'": '"',
}
QUOTE_REGEX = re.compile("|".join(STRING_QUOTES))
ESCAPE_SEQUENCES = {fr"\{q}": q for q in STRING_QUOTES}
ESCAPE_SEQUENCES[r"\\"] = "\\"
ESCAPE_SUBS = dict(reversed(tuple(map(reversed, ESCAPE_SEQUENCES.items()))))

def get_writer(indent: int = 4):
    return Writer(indent=indent)

class Writer:
    def __init__(self, indent: int = 4):
        self.indentation = " " * indent
        
        self.indent = ""
        self.previous_indent = ""
        
    @contextmanager
    def depth(self):
        if self.indentation is None:
            yield
        else:
            previous = self.previous_indent
            self.previous_indent = self.indent
            self.indent += self.indentation
            yield
            self.indent = self.previous_indent
            self.previous_indent = previous
            
    def should_expand(self, tag):
        return (
            self.indentation is not None
            and tag
            and (
                not self.previous_indent
                or (
                    isinstance(tag, List)
                    and len(tag) > 1
                )
                or isinstance(tag, Compound)
            )
        )

    def expand(self, fmt):
        return (
            f"\n{self.indent}",
            fmt.replace("{}", f"\n{self.indent}{{}}\n{self.previous_indent}"),
        )

    def write(self, tag: Base) -> str:
        if isinstance(tag, Compound):
            return self.write_compound(tag)
        elif isinstance(tag, List):
            return self.write_list(tag)
        elif isinstance(tag, Numeric):
            return self.write_numeric(tag)
        elif isinstance(tag, String):
            return self.write_string(tag)
        elif isinstance(tag, Bool):
            return "true" if tag else "false"
        return f"{tag}"
    
    def write_numeric(self, tag: Numeric) -> str:
        func = int.__repr__ if isinstance(tag, int) else float.__repr__
        return f"{func(tag)}{tag.suffix}"
    
    def write_string(self, tag: String) -> str:
        found = QUOTE_REGEX.search(tag)
        quote = STRING_QUOTES[found.group()] if found else next(iter(STRING_QUOTES))

        for match, seq in ESCAPE_SUBS.items():
            if match == quote or match not in STRING_QUOTES:
                tag = tag.replace(match, seq)
        return f"{quote}{tag}{quote}"
    
    def write_list(self, tag: List) -> str:
        separator, fmt = "\n", "[{}]"

        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(fmt)
                
            if len(tag) == 0:
                return "[ ]"

            return fmt.format(separator.join(map(self.write, tag)))
    
    def write_compound(self, tag: Compound) -> str:
        separator, fmt = "\n", "{{{}}}"

        with self.depth():
            if self.should_expand(tag):
                separator, fmt = self.expand(fmt)
            
            if len(tag) == 0:
                return "{ }"

            return fmt.format(
                separator.join(
                    f"{self.stringify_compound_key(key)}: {self.write(value)}"
                    for key, value in tag.items()
                )
            )
            
    def stringify_compound_key(self, key):
        if isinstance(key, String):
            return self.write_string(key)
        return key