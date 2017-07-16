from flask import Flask ,request
import flask_restful
import sys
import decimal
sys.path.append('../')
from DataBase.SqlConnector import *


app = Flask(__name__, static_url_path='')
api = flask_restful.Api(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

#class HelloWorld(flask_restful.Resource):
#    def get(self):
#        return app.send_static_file('html/index.html')

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
            #elif isinstance(obj, date):
            #return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, bytearray) :
            return obj.decode('utf8')
        else:
            return json.JSONEncoder.default(self, obj)

class MaterialVisual(flask_restful.Resource) :
    def get(self, page_id) :
        data, pages = VisualData().GetMaterialVisuals(page_id, 12)
        return json.dumps({'data':data, 'page_index':page_id}, cls = CJsonEncoder)

class PlanetsVisual(flask_restful.Resource) :
    def get(self, page_id) :
        data, pages = VisualData().GetPlanetVisuals(page_id, 12)
        return json.dumps({'data':data, 'page_index':page_id}, cls = CJsonEncoder)

class PlanetDetail(flask_restful.Resource) :
    def get(self, planet_id) :
        data = VisualData().GetPlanetDetail(planet_id)
        return json.dumps(data, cls = CJsonEncoder)

class SpaceVisuals(flask_restful.Resource) :
    def get(self) :
        data = VisualData().GetSpaceVisuals()
        return data

class Logs(flask_restful.Resource) :
    def get(self, page_id) :
        data, pages =  LogData().GetLog(page_id, 50)
        return json.dumps({'data':data, 'page_index':page_id}, cls = CJsonEncoder)

class Tasks(flask_restful.Resource) :
    def get(self) :
        return json.dumps(TaskData().GetTasks("render"), cls = CJsonEncoder)

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
api.add_resource(MaterialVisual, '/api/materials/<int:page_id>')
api.add_resource(PlanetsVisual, '/api/planets/<int:page_id>')
api.add_resource(PlanetDetail, '/api/planetdetail/<int:planet_id>')
api.add_resource(Logs, '/api/logs/<int:page_id>')
api.add_resource(Tasks, '/api/tasks')
api.add_resource(SetTasks, '/api/settasks')

if __name__ == '__main__':
    app.run(debug=True)
