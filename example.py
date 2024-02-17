from ftb_snbt_parser import get_parser
import json

# Get the parser object
parser = get_parser()

# Read the FTB SNBT file
with open("tests/medium_voltage.snbt", "r") as f:
    snbt = f.read()
    
# Parse the FTB SNBT file and return the result as a dictionary
result = parser.parse(snbt)

# Save the result as a JSON file
json.dump(result, open("tests/medium_voltage.json", "w"), indent=4, ensure_ascii=False)