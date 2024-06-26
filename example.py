import ftb_snbt_lib as slib
import json

# Load the ftb snbt tag from a file.
some_snbt = slib.load(open("tests/some_file.snbt", "r", encoding="utf-8"))

# Dump the ftb snbt tag to a file.
slib.dump(some_snbt, open("tests/some_file_copy.snbt", "w", encoding="utf-8"))

# Load the ftb snbt tag from a string.
another_snbt = slib.loads('''
{
    some_tag: "some_value"
    another_tag: 1b
}
''')

# Dump the ftb snbt tag to a string.
dumped_snbt = slib.dumps(another_snbt)

# Print the dumped snbt string.
print(dumped_snbt)
# Output:
# {
#     some_tag: "some_value"
#     another_tag: 1b
# }

# Edit the snbt tag. Since the snbt tag is a Compound, it can be edited like a dictionary but only with custom types provided by this library.
another_snbt["some_tag"] = slib.String("another_value")

# Save the edited snbt tag to a json file.
json.dump(another_snbt, open("tests/test.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)