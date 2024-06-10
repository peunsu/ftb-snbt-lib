# ftb-snbt-lib

![GitHub Release](https://img.shields.io/github/v/release/peunsu/ftb-snbt-lib?style=for-the-badge)

**A python library to parse, edit, and save FTB snbt tag.**

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
>>> import ftb_snbt_lib as slib
```

* ``load(fp)``: Load the ftb snbt tag from a file (``fp``).<br>
The type of returned value is ``Compound``, a dictionary-like object.<br>
The ``Compound`` is containing values with **[tag data types](#data-types)** provided by this library.

```python
>>> some_snbt = slib.load(open("tests/some_file.snbt", "r", encoding="utf-8"))
>>> type(some_snbt)
<class 'ftb_snbt_lib.tag.Compound'>
>>> print(some_snbt)
Compound({'some_tag': String('some_value'), 'another_tag': Byte(1)})
```

* ``dump(tag, fp, comma_sep=False)``: Dump the ftb snbt tag to a file (``fp``).<br>
If you set ``comma_sep`` parameter to ``True``, the output snbt has comma separator ``,\n`` instead of non-comma separator ``\n``.

```python
>>> slib.dump(some_snbt, open("tests/some_file_copy.snbt", "w", encoding="utf-8"))
# File Output:
# {
#    some_tag: "some_value"
#    another_tag: 1b
# }
```

```python
>>> slib.dump(some_snbt, open("tests/some_file_copy.snbt", "w", encoding="utf-8"), comma_sep=True)
# File Output:
# {
#    some_tag: "some_value",
#    another_tag: 1b
# }
```

* ``loads(s)``: Load the ftb snbt tag from a string ``s``.<br>
The type of returned value is ``Compound``.

```python
>>> another_snbt = slib.loads('''
... {
...     some_tag: "some_value"
...     another_tag: 1b
... }
... ''')
>>> type(another_snbt)
<class 'ftb_snbt_lib.tag.Compound'>
>>> print(another_snbt)
Compound({'some_tag': String('some_value'), 'another_tag': Byte(1)})
```

* ``dumps(tag, comma_sep=False)``: Dump the ftb snbt tag to a string.<br>
If you set ``comma_sep`` parameter to ``True``, the output snbt has comma separator ``,\n`` instead of non-comma separator ``\n``.

```python
>>> dumped_snbt = slib.dumps(another_snbt)
>>> print(dumped_snbt)
{
    some_tag: "some_value"
    another_tag: 1b
}
```

```python
>>> dumped_snbt = slib.dumps(another_snbt, comma_sep=True)
>>> print(dumped_snbt)
{
    some_tag: "some_value",
    another_tag: 1b
}
```

* Edit the snbt tag. As its type is ``Compound``, it can be edited like a dictionary.<br>
The inserted or replace values should be any of **[tag data types](#data-types)** provided by this library.

```python
>>> another_snbt["some_tag"] = slib.String("another_value")
```

* When editing the ``List``, a list-like object, its elements must have **the same type**.<br>
For instance, ``List[Byte(1), Byte(2), Byte(3)]`` must contain **only** the ``Byte`` type object, so the other types like ``Integer`` or ``String`` **cannot be added or replaced** in it.

* When editing the ``Array``, a list-like object with **a fixed length**, its elements must have **the same type**, and that type must **match the element type defined in the array**.<br>
For instance, ``IntArray`` with a length of 3 must contain **three** ``Integer`` type objects, so **adding new objects, removing existing objects, and replacing with other type objects are not allowed**.

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
| Float | A 32-bit, single-precision floating-point number.<br>Range: ``-3.4E+38`` ~ ``+3.4E+38`` | ``<number>f`` | ``12.345f``, ``1.0E-6f`` |
| Double | A 64-bit, double-precision floating-point number.<br>Range: ``-1.7E+308`` ~ ``+1.7E+308`` | ``<number>d`` | ``12.345d``, ``1.0E-6d`` |
| Bool | A boolean data type.<br>``0`` for ``false``, ``1`` for ``true``. | ``false``, ``true`` | ``true`` |
| String | A sequence of characters. | A string enclosed in **double quotes ``""``**.<br>Nested double quotes can be included within a string using a **escaping character ``\"``**. | `"Hello, World!"`,<br>`"Say \"Hello, World!\""` |
| List | An ordered list of tags.<br>The tags must be of **the same type**, determined by the first tag in the list. | Unnamed tags enclosed in square brackets and delimited by **newline** characters (``\n``). | <pre>[<br>    3.2d<br>    1.4d<br>    ...<br>]</pre> |
| Array | An ordered list of 8-bit(``ByteArray``), 32-bit(``IntArray``), 64-bit(``LongArray``) integers. | ``<array_prefix>;`` followed by an ordered list of tags enclosed in square brackets and delimited by **newline** characters (``\n``).<br>Valid array prefixes are ``B``(Byte), ``I``(Integer), and ``L``(Long). | <pre>[B;<br>    12b<br>    -35b<br>    ...<br>]</pre> |
| Compound | An ordered list of attribute-value pairs.<br>Each tag can be of **any type**. | Named tags enclosed in curly braces and delimited by commas or **newline** characters (``\n``).<br>The key (tag name) can be unquoted if it contains only ``0-9``, ``A-Z``, ``a-z``, ``_``, ``-``, ``.``, and ``+``. Otherwise the key should be quoted, using the format of ``String`` type. | <pre>[<br>    tag1: "string"<br>    tag2: 12b<br>    \"quoted:tag\": 3.5d<br>    ...<br>]</pre> |

## References

* [PLY - Python Lex-Yacc](https://github.com/dabeaz/ply) by [David Beazley](https://www.dabeaz.com)
* [nbtlib](https://github.com/vberlier/nbtlib) by [vberlier](https://github.com/vberlier)
* [NBT format - Minecraft Wiki (fandom)](https://minecraft.fandom.com/wiki/NBT_format)