import pkgutil
import os
import encodings

def all_encodings():
    modnames = set(
        [modname for importer, modname, ispkg in pkgutil.walk_packages(
            path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)

filename = '/save/ngupta19/crosswikis/data/ss'
encodings = all_encodings()
for enc in encodings:
    try:
        with open(filename, encoding=enc) as f:
            # print the encoding and the first 500 characters
            print(enc, f.read(500))
    except Exception:
        pass