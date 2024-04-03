# ftb-snbt-lib
A python library to parse, edit, and save FTB snbt tag.

The FTB snbt tag is a variant of the "vanilla" snbt tag. It has no commas at end of lines, different suffixes for numeric values, and no support for array data type.

This is the example of the FTB snbt tag:
```python
{
    some_tag: "some_value"
    another_tag: 1b
    list_tag: [
        "a"
        "b"
        "c"
    ]
}
```

**This library is only for the FTB snbt tag**. If you are finding the snbt library for the "vanilla" snbt tag, use [nbtlib](https://github.com/vberlier/nbtlib) by [vberlier](https://github.com/vberlier).

## Installation
The package can be installed with ``pip``.
```bash
$ pip install ftb-snbt-lib
```

## Getting Started
* Import the library.
```python
>>> import ftb_snbt_lib
```

* ``load(fp)``: Load the ftb snbt tag from a file (``fp``).
```python
>>> some_snbt = ftb_snbt_lib.load(open("tests/some_file.snbt", "r", encoding="utf-8"))
```
* The type of returned value is ``Compound``, a dictionary-like object.<br>
The ``Compound`` is containing values with **[tag data types](#data-types)** provided by this library.
```python
>>> type(some_snbt)
<class 'ftb_snbt.tag.Compound'>
>>> print(some_snbt)
Compound({'some_tag': String('some_value'), 'another_tag': Byte(1)})
```

* ``dump(tag, fp)``: Dump the ftb snbt tag to a file (``fp``).
```python
>>> ftb_snbt_lib.dump(some_snbt, open("tests/some_file_copy.snbt", "w", encoding="utf-8"))
```

* ``loads(s)``: Load the ftb snbt tag from a string ``s``.
```python
>>> another_snbt = ftb_snbt_lib.loads('''
... {
...     some_tag: "some_value"
...     another_tag: 1b
... }
... ''')
```

* ``dumps(tag)``: Dump the ftb snbt tag to a string.
```python
>>> dumped_snbt = ftb_snbt_lib.dumps(another_snbt)
>>> print(dumped_snbt)
{
    some_tag: "some_value"
    another_tag: 1b
}
```

* Edit the snbt tag. As its type is ``Compound``, it can be edited like a dictionary.<br>
The inserted or replace values should be any of **[tag data types](#data-types)** provided by this library.
```python
>>> another_snbt["some_tag"] = ftb_snbt_lib.String("another_value")
```

* When editing the ``List``, a list-like object, its elements must have **the same type**.<br>
For instance, ``List[Byte(1), Byte(2), Byte(3)]`` must contain **only** the ``Byte`` type object, so the other types like ``Integer`` or ``String`` **cannot be added or replaced** in it.

* Save the edited snbt tag to a json file.
```python
>>> import json
>>> json.dump(another_snbt, open("tests/test.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
```

## Data Types
| Type | Description | Format | Example |
| - | - | - | - |
| Byte | A signed 8-bit integer.<br>Range: ``-128`` ~ ``127`` | ``<number>b`` | ``12b``, ``-35b`` |
| Short | A signed 16-bit integer.<br>Range: ``-32,768`` ~ ``32,767`` | ``<number>s`` | ``132s``, ``-243s`` |
| Integer | A signed 32-bit integer.<br>Range: ``-2,147,483,647`` ~ ``2,147,483,647`` | ``<number>`` | ``12345`` |
| Long | A signed 64-bit integer.<br>Range: ``9,223,372,036,854,775,808`` ~ ``9,223,372,036,854,775,807`` | ``<number>L`` | ``12345L`` |
| Double | A 64-bit, double-precision floating-point number.<br>Range: ``-1.7E+308`` ~ ``+1.7E+308.`` | ``<number>d`` | ``12.345d`` |
| Bool | A boolean data type.<br>``0`` for ``false``, ``1`` for ``true``. | ``false``, ``true`` | ``true`` |
| String | A sequence of characters. | A string enclosed in **double quotes ``""``**.<br>Nested double quotes can be included within a string using a **escaping character ``\"``**. | `"Hello, World!"`,<br>`"Say \"Hello, World!\""` |
| List | An ordered list of tags.<br>The tags must be of **the same type**, determined by the first tag in the list. | Unnamed tags enclosed in square brackets and delimited by **newline** characters (``\n``). | <pre>[<br>    3.2d<br>    1.4d<br>    ...<br>]</pre> |
| Compound | An ordered list of attribute-value pairs.<br>Each tag can be of **any type**. | Named tags enclosed in curly braces and delimited by commas or **newline** characters (``\n``).<br>The key (tag name) can be unquoted if it contains only ``0-9``, ``A-Z``, ``a-z``, ``_``, ``-``, ``.``, and ``+``. Otherwise the key should be quoted, using the format of ``String`` type. | <pre>[<br>    tag1: "string"<br>    tag2: 12b<br>    \"quoted:tag\": 3.5d<br>    ...<br>]</pre> |

## References
* [PLY - Python Lex-Yacc](https://github.com/dabeaz/ply) by [David Beazley](https://www.dabeaz.com)
* [nbtlib](https://github.com/vberlier/nbtlib) by [vberlier](https://github.com/vberlier)