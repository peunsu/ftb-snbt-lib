import ftb_snbt_lib
import json

# Load the ftb snbt tag from a file.
some_snbt = ftb_snbt_lib.load(open("tests/medium_voltage.snbt", "r", encoding="utf-8"))

# Dump the ftb snbt tag to a file.
ftb_snbt_lib.dump(some_snbt, open("tests/medium_voltage_copy.snbt", "w", encoding="utf-8"))

# Load the ftb snbt tag from a file.
some_snbt = ftb_snbt_lib.load(open("tests/ad_astra.snbt", "r", encoding="utf-8"))

# Dump the ftb snbt tag to a file.
ftb_snbt_lib.dump(some_snbt, open("tests/ad_astra_copy.snbt", "w", encoding="utf-8"))