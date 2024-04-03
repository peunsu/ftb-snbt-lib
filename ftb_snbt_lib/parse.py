from .ply import yacc
from .token import tokens
from .tag import *

__all__ = ["get_parser", "loads", "load"]

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
        p[0] = p[1] + [p[3]]
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
                | SHORT
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

def get_parser():
    """Get the FTB snbt parser object.
    
    The parser object is ``yacc`` parser object that can be used to parse FTB snbt strings.
    
    Example
    -------
        >>> import ftb_snbt
        >>> parser = ftb_snbt.get_parser()
        >>> snbt = parser.parse('''
            {
                some_tag: "some_value"
                another_tag: 1b
            }
            ''')
        >>> print(snbt)
        Compound({'some_tag': String('some_value'), 'another_tag': Byte(1)})
    """
    return yacc.yacc()

def loads(s: str) -> Compound:
    """Load an FTB snbt string and return the result as a Compound object.
    
    The loaded SNBT object consists of custom types: ``Compound``, ``List``, ``Numeric``, ``Bool``, and ``String``.
    
    When modifying the loaded object, use the provided custom types to ensure that the object is valid.

    Args
    ----
        s (str): The FTB snbt string to parse.

    Returns
    -------
        Compound: The loaded FTB snbt Compound object.
        
    Example
    -------
        >>> import ftb_snbt
        >>> snbt = ftb_snbt.loads('''
            {
                some_tag: "some_value"
                another_tag: 1b
            }
            ''')
        >>> print(snbt)
        Compound({'some_tag': String('some_value'), 'another_tag': Byte(1)})
    """
    parser = get_parser()
    return parser.parse(s)

def load(fp) -> Compound:
    """    
    Load an FTB snbt file and return the result as a Compound object.
    
    The loaded SNBT object consists of custom types: ``Compound``, ``List``, ``Numeric``, ``Bool``, and ``String``.
    
    When modifying the loaded object, use the provided custom types to ensure that the object is valid.

    Args
    ----
        fp (``io.TextIOWrapper``): The FTB snbt file to parse (opened in reading text mode with a ``UTF-8`` encoding.)

    Returns
    -------
        Compound: The loaded FTB snbt Compound object.
        
    Example
    -------
        >>> import ftb_snbt
        >>> snbt = ftb_snbt.load(open("path/to/file/some_file.snbt", "r", encoding="utf-8"))
        >>> type(snbt)
        <class 'ftb_snbt.tag.Compound'>
    """
    parser = get_parser()
    return parser.parse(fp.read())