from .ply import yacc
from .token import tokens
from .tag import *

def p_snbt(p):
    """snbt : compound"""
    p[0] = p[1]

def p_compound(p):
    """compound : LBRACE key_value_pairs RBRACE
                | LBRACE RBRACE"""
    if len(p) == 3:
        p[0] = Compound()
    else:
        p[0] = Compound(p[2])

def p_key_value_pairs(p):
    """key_value_pairs : key_value_pairs key_value_pair
                       | key_value_pairs COMMA key_value_pair
                       | key_value_pair"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]

def p_key_value_pair(p):
    """key_value_pair : NAME COLON value
                      | STRING COLON value"""
    p[0] = (p[1], p[3])

def p_value(p):
    """value : compound
                | list
                | BOOL
                | BYTE
                | DOUBLE
                | LONG
                | INTEGER
                | STRING"""
    p[0] = p[1]

def p_list(p):
    """list : LBRACKET values RBRACKET
                | LBRACKET RBRACKET"""
    if len(p) == 3:
        p[0] = List()
    else:
        p[0] = List(p[2])

def p_values(p):
    """values : values value
              | values COMMA value
              | value"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = p[1] + [p[2]]
    
def p_error(p):
    raise ValueError(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}, type {p.type}")

def get_parser() -> yacc.LRParser:
    return yacc.yacc()