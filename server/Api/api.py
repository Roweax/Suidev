from flask import Flask ,request
import flask_restful
import sys
sys.path.append('../')
from DataBase.SqlConnector import *


app = Flask(__name__, static_url_path='')
api = flask_restful.Api(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

class HelloWorld(flask_restful.Resource):
    def get(self):
        return app.send_static_file('html/index.html')

class MaterialVisual(flask_restful.Resource) :
    def get(self) :
        return VisualData().GetMaterialVisuals()

class PlanetsVisual(flask_restful.Resource) :
    def get(self) :
        return VisualData().GetPlanetVisuals()

class SpaceVisuals(flask_restful.Resource) :
    def get(self) :
        data = VisualData().GetSpaceVisuals()
        return data

class Logs(flask_restful.Resource) :
    def get(self) :
        return LogData().GetLog()

class Tasks(flask_restful.Resource) :
    def get(self) :
        return TaskData().GetTasks("render")

class SetTasks(flask_restful.Resource) :
    def put(self) :
        tasks = request.get_json()
        return TaskData().SetTasks(tasks)


class Todo2(flask_restful.Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201


class Todo3(flask_restful.Resource):
    def get(self):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}

#api.add_resource(HelloWorld, '/')
api.add_resource(MaterialVisual, '/api/materials')
api.add_resource(Logs, '/api/logs')
api.add_resource(Tasks, '/api/tasks')
api.add_resource(SetTasks, '/api/settasks')

if __name__ == '__main__':
    app.run(debug=True)
