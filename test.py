from ftb_snbt_parser.tag import *

mycompound = Compound({"a": Integer(1)})
print(mycompound)
mylist = List([mycompound, mycompound])
print(mylist)