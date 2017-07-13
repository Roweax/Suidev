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
def resize(in_file, out_file, width) :
    im = Image.open(in_file)  
    (x, y) = im.size   
    x_s = width
    y_s = int(1.0 * y / x * width)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(out_file)

#if __name__ == "main2":

temp_file = Config.data_path + "temp2/0001.png"
temp_file2 = Config.data_path + "temp2/0002.png"
temp_file3 = Config.data_path + "temp2/0003.png"
while True :
    kind = "space"
    render_task_data = shelve.open(Config.data_path + "temp/render.dat")
    render_task_data["kind"] = kind
    render_task_data.close();
    
    if os.path.exists(temp_file) :
        os.remove(temp_file)

    start = datetime.now()
    print os.system('blender -b -noaudio -P BlenderImporter/Run2.py')
    end = datetime.now()
    escape = (end - start).seconds
    print(escape)
    time.sleep(5)

    if os.path.exists(temp_file):
        render_data_file = shelve.open(Config.data_path +  "temp/render.dat")
        state = render_data_file["render"]
        render_data_file.close()
        
        if kind == "scene":
            visual = VisualData()
            m_id = visual.AddMaterial("", state.color, state.material_name)
            v_id = visual.AddMaterialVisual(m_id, state.width, state.height, state.file_format, state.sample, escape, state.scene, state.model)
            del visual
            #visual.AddMaterialVisual()
            aliyun_oss = AliyunOSS()
            aliyun_oss.Save(temp_file, "render/material/original/{0:08X}.png".format(v_id))
            resize(temp_file, temp_file2, 400)
            aliyun_oss.Save(temp_file2, "render/material/middle/{0:08X}.png".format(v_id)) 
            resize(temp_file, temp_file3, 100)
            aliyun_oss.Save(temp_file3, "render/material/small/{0:08X}.png".format(v_id))
        elif kind == "space":
            aliyun_oss = AliyunOSS()
            aliyun_oss.Save(Config.data_path + "temp2/0001.png", "render/space.png")
