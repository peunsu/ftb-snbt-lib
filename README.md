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

## Example
```python
import ftb_snbt_lib
import json

# Load the ftb snbt tag from a file.
some_snbt = ftb_snbt_lib.load(open("tests/some_file.snbt", "r", encoding="utf-8"))

# Dump the ftb snbt tag to a file.
ftb_snbt_lib.dump(some_snbt, open("tests/some_file_copy.snbt", "w", encoding="utf-8"))

# Load the ftb snbt tag from a string.
another_snbt = ftb_snbt_lib.loads('''
{
    some_tag: "some_value"
    another_tag: 1b
}
''')

# Dump the ftb snbt tag to a string.
dumped_snbt = ftb_snbt_lib.dumps(another_snbt)

# Print the dumped snbt string.
print(dumped_snbt)
# Output:
# {
#     some_tag: "some_value"
#     another_tag: 1b
# }

# Edit the snbt tag. Since the snbt tag is a Compound, it can be edited like a dictionary but only with custom types provided by this library.
another_snbt["some_tag"] = ftb_snbt_lib.String("another_value")

# Save the edited snbt tag to a json file.
json.dump(another_snbt, open("tests/test.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
```

## References
* [PLY - Python Lex-Yacc](https://github.com/dabeaz/ply) by [David Beazley](https://www.dabeaz.com)
* [nbtlib](https://github.com/vberlier/nbtlib) by [vberlier](https://github.com/vberlier)