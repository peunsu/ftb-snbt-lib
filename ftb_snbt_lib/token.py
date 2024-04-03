from .ply import lex
from .tag import *
    
tokens = (
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "BOOL",
    "BYTE",
    "SHORT",
    "DOUBLE",
    "LONG",
    "INTEGER",
    "STRING",
    "NAME",
    "COLON",
    "COMMA",
)

t_ignore = ' \t\r'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_LBRACE(t):
    r'\{'
    t.lexer.level += 1
    return t

def t_RBRACE(t):
    r'\}'
    t.lexer.level -= 1
    return t

def t_LBRACKET(t):
    r'\['
    t.lexer.level += 1
    return t

def t_RBRACKET(t):
    r'\]'
    t.lexer.level -= 1
    return t

def t_BOOL(t):
    r'true|false'
    t.value = Bool(t.value == "true")
    return t

def t_BYTE(t):
    r'\-?[0-9]+b'
    t.value = Byte(t.value[:-1])
    return t

def t_SHORT(t):
    r'\-?[0-9]+s'
    t.value = Short(t.value[:-1])
    return t

def t_DOUBLE(t):
    r'\-?[0-9]+\.[0-9]+d'
    t.value = Double(t.value[:-1])
    return t

def t_LONG(t):
    r'\-?[0-9]+L'
    t.value = Long(t.value[:-1])
    return t

def t_INTEGER(t):
    r'\-?[0-9]+'
    t.value = Integer(t.value)
    return t

def t_STRING(t):
    r'\"[^\"\\]*(?:\\.[^\"\\]*)*\"'
    t.value = String(t.value[1:-1].replace(r'\"', '"').replace(r'\\', '\\'))
    return t

def t_NAME(t):    
    r'[a-zA-Z0-9._+-]+'
    return t

def t_COLON(t):
    r'\:'
    return t

def t_COMMA(t):
    r'\,'
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()
lexer.level = 0