import sys
import os
import shelve
sys.path.append("/root/develop/suidev/")
sys.path.append("/root/develop/suidev/server/BlenderImporter/")

print("Blender Script  run at %s", sys.executable)
print("Script File path is %s", sys.path[0])

from Importer import Importer
from Config import Config

render_task = shelve.open(Config.data_path + "temp/render.dat", protocol=2, writeback=True)


importer = Importer()
importer.Render(Config.resource_path + render_task["kind"] + ".json")

render_task.close()

