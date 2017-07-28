import sys
import os
import shelve
import dbm
sys.path.append("/root/develop/suidev/server/")
sys.path.append("/root/develop/suidev/server/BlenderImporter/")

print("Blender Script  run at %s", sys.executable)
print("Script File path is %s", sys.path[0])

from Importer import Importer
from Config import Config

#render_task = shelve.Shelf(dbm.open(Config.data_path + "temp/render", 'r'))
render_task = shelve.open(Config.data_path + "temp/render", protocol=2, writeback=True)
kind = render_task["kind"]
render_task.close()
importer = Importer()
importer.Render(kind)

