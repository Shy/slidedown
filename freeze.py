from flask_frozen import Freezer
from app import app
import contentful
import os
import shutil

SPACE_ID = os.environ.get("SPACE_ID")
DELIVERY_API_KEY = os.environ.get("DELIVERY_API_KEY")

client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)

freezer = Freezer(app)


@freezer.register_generator
def deck_by_id():
    decks = client.entries({"content_type": "slideDeck"})
    for deck in decks:
        yield {"deck_id": deck.id}

def copytree(src, dst, symlinks = False, ignore = None):
  if not os.path.exists(dst):
    os.makedirs(dst)
    shutil.copystat(src, dst)
  lst = os.listdir(src)
  if ignore:
    excl = ignore(src, lst)
    lst = [x for x in lst if x not in excl]
  for item in lst:
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if symlinks and os.path.islink(s):
      if os.path.lexists(d):
        os.remove(d)
      os.symlink(os.readlink(s), d)
      try:
        st = os.lstat(s)
        mode = stat.S_IMODE(st.st_mode)
        os.lchmod(d, mode)
      except:
        pass # lchmod not available
    elif os.path.isdir(s):
      copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)

if __name__ == "__main__":
    freezer.freeze()
    source = "reveal.js"
    destination = "build"
    # create a backup directory
    copytree(source, destination)
