import sys
from testmodule import *
from os import listdir
from os.path import join
import empty

toignore = set(dir(empty))
hashes = {}
fntype = type(lambda x: x)

def test():
    mod = getCurMod()
    modname = getCurModName()
    for fn_name in dir(mod):
        if not fn_name in toignore:
            try:
                fn = getattr(mod, fn_name)
                if type(fn) == fntype:
                    code = fn.__code__.co_code
                    bucket = hashes.get(code, [])
                    bucket.append((modname, fn_name))
                    if len(bucket) == 1:
                        hashes[code] = bucket
            except:
                pass # not a function

if __name__ == "__main__":
    files = [x for x in listdir(sandpit) if x.endswith(".py")]
    
    for fname in files:
        beginTests(test, {
            "filename": fname.split(".py")[0],
        })
        
    for code in hashes:
        names = hashes[code]
        if len(names) > 1:
            print("same bytecode: ", names)
