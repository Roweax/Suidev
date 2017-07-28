import sys
import os
import shelve
import time
from PIL import Image
from OSS.oss import AliyunOSS
from DataBase.SqlConnector import *
from Config import Config
sys.path.append("BlenderImporter")
sys.path.append("Resource")
import State
import Color
import random
import dumbdbm

def resize(in_file, out_file, width) :
    im = Image.open(in_file)
    (x, y) = im.size
    x_s = width
    y_s = int(1.0 * y / x * width)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(out_file)

def GetTask() :
    return "geomtery"

def ClearFiles() :
    DeleteFiles(Config.data_path + "temp/", "png")
    DeleteFiles(Config.data_path + "temp/", "mp4")
    DeleteFiles(Config.data_path + "temp/", "mov")

def DeleteFiles(path, ext):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith("." + ext):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))

def SaveTempToOSS() :
    aliyun_oss = AliyunOSS()
    print("Save Temp Files:")
    path = Config.data_path + "temp/"
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".mp4") or name.endswith(".png") or name.endswith(".mov"):
                aliyun_oss.Save(os.path.join(root, name), "render/" + name)

if __name__ == "__main__":

    temp_file = Config.data_path + "temp/0000.png"
    temp_file2 = Config.data_path + "temp/0002.png"
    temp_file3 = Config.data_path + "temp/0003.png"
    temp_file_mp4 = Config.data_path + "temp/0001-0200.mp4"

    while True :
        task = GetTask()

        render_task_data = shelve.open(Config.data_path + "temp/render", protocol=2, writeback=True)
        #render_task_data = shelve.Shelf(dumbdbm.open(Config.data_path + "temp/render", 'w'))
        render_task_data["kind"] = task
        render_task_data.close();
        
        ClearFiles()

        if task == "geomtery" :
            aliyun_oss = AliyunOSS()
            task_list = aliyun_oss.List("task")
            print(task_list[0])
            aliyun_oss.Load(task_list[0], Config.resource_path + "task.json")

        start = datetime.now()
        #os.system('export PATH=/root/develop/blender-2.78c/:$PATH')
        os.system('export PATH=/root/develop/blender-2.78c:$PATH\n  blender -b -noaudio -P BlenderImporter/Run.py')
        end = datetime.now()
        escape = (end - start).seconds
        print(escape)

        render_data_file = shelve.open(Config.data_path + "temp/render")
        state = render_data_file["render"]
        render_data_file.close()

        if task == "scene":
            if os.path.exists(temp_file):
                visual = VisualData()
                m_id = visual.AddMaterial("", state.color, state.material_name)
                v_id = visual.AddMaterialVisual(m_id, state.width, state.height, state.file_format, state.sample, escape, state.scene, state.model)
                del visual
                aliyun_oss = AliyunOSS()
                aliyun_oss.Save(temp_file, "render/material/original/{0:08X}.png".format(v_id))
                resize(temp_file, temp_file2, 400)
                aliyun_oss.Save(temp_file2, "render/material/middle/{0:08X}.png".format(v_id))
                resize(temp_file, temp_file3, 100)
                aliyun_oss.Save(temp_file3, "render/material/small/{0:08X}.png".format(v_id))
        elif task == "space":
            SaveTempToOSS()
            result = State.instance.Get("result") 
            planet = State.instance.Get("planet")
            if len(result) == 13:
                visual = VisualData()
                aliyun_oss = AliyunOSS()
                p_id = visual.AddPlanet(planet["kind"], planet["ring"], Config.server_name)
                for r in result :
                    v_id = visual.AddPlanetVisual(p_id, r["x"], r["y"], r["sample"], r["fps"], r["length"], r["frame"], r["format"], r["render_time"], r["rotate"], r["light_angle"])
                    if r["format"] == "PNG":
                        temp_original = Config.data_path + "temp/{0:04d}.png".format(r["frame"])
                        temp_middle = Config.data_path + "temp/{0:04d}_m.png".format(r["frame"])
                        temp_small = Config.data_path + "temp/{0:04d}_s.png".format(r["frame"])
                        resize(temp_original, temp_middle, 300)
                        resize(temp_original, temp_small, 100)
                        aliyun_oss.Save(temp_original, "render/planet/original/{0:08X}.png".format(v_id))
                        aliyun_oss.Save(temp_middle, "render/planet/middle/{0:08X}.png".format(v_id))
                        aliyun_oss.Save(temp_small, "render/planet/small/{0:08X}.png".format(v_id))

                    else :
                        aliyun_oss.Save(Config.data_path + "temp/0000-0239.mp4", "render/planet/video/{0:08X}.mp4".format(p_id))
                del visual
        elif task == "geomtery":
            SaveTempToOSS()


        time.sleep(5)
