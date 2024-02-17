from ftb_snbt_parser import get_parser
import json

parser = get_parser()
with open("tests/medium_voltage.snbt", "r") as f:
    snbt = f.read()
result = parser.parse(snbt)
json.dump(result, open("tests/medium_voltage.json", "w"), indent=4, ensure_ascii=False)