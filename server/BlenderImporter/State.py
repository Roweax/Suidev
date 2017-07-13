import shelve
from Config import Config

class State(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.sample = 0
        self.file_format =""
        self.material_name = ""
        self.scene = ""
        self.model = ""
        self.task = None

    def Set(self, name, value) :
        render_data_file = shelve.open(Config.data_path + "temp/render", protocol=2)
        render_data_file[name] = value
        render_data_file.close()

    
    def Get(self, name) :
        render_data_file = shelve.open(Config.data_path + "temp/render", protocol=2)
        value = render_data_file[name]
        render_data_file.close()
        return value
instance = State()
    
