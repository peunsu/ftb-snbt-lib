# ftb-snbt-parser
A python library to parse and edit FTB snbt format data which has no commas at end of lines.

## Example
```python
from ftb_snbt_parser import get_parser, get_writer
import json

# Get the parser object
parser = get_parser()

# # Read the FTB SNBT file
with open("tests/hello_world.snbt", "r") as f:
    snbt = f.read()
    
# Parse the FTB SNBT file and return the result as a dictionary
result = parser.parse(snbt)

# Get the writer object
writer = get_writer()

# Save the dictionary as a FTB SNBT file
with open("tests/hello_world_copy.snbt", "w") as f:
    f.write(writer.write(result))

# ...or save it as a JSON file
json.dump(result, open("tests/hello_world.json", "w"), indent=4, ensure_ascii=False)
```

## Acknowledgements
* [PLY - Python Lex-Yacc](https://github.com/dabeaz/ply) by [David Beazley](https://www.dabeaz.com)
* [nbtlib](https://github.com/vberlier/nbtlib) by [vberlier](https://github.com/vberlier)