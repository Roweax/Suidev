import mysql.connector
import json
from datetime import datetime
from DBUtils.PooledDB import PooledDB
import DBUtils.PersistentDB
from Config import Config
import BlenderImporter.Color
class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
            #elif isinstance(obj, date):
            #return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytearray) :
            return obj.decode('utf8')
        else:
            return json.JSONEncoder.default(self, obj)

class SqlConnector(object):

    pool =PooledDB(creator=mysql.connector, mincached=1 , maxcached=20, host=Config.sql_path, port=Config.sql_port , user=Config.sql_user , passwd=Config.sql_password , db=Config.sql_database, use_unicode=False)
    def __init__(self) :
        self.conn = SqlConnector.pool.connection()
        self.cur = self.conn.cursor(dictionary=True)

    def __del__(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def GetPintures(self, page, kind):
        self.cur.execute("SELECT * from suidev_render")
        #return json.dumps(self.cur.fetchall(), cls=CJsonEncoder)
        return self.cur.fetchall()

class SpaceData(SqlConnector) :
    def __init__(self) :
        super(SpaceData, self).__init__()

    def __del__(self) :
        super(SpaceData, self).__del__()

    def AddSpace(self, name) :
        insert_cmd = "INSERT INTO suidev_space (name, create_time) VALUE(%s, %s)"
        insert_data = (name, datetime.now())
        self.cur.execute(insert_cmd, insert_data)

    def GetSpaces(self):
        self.cur.execute('SELECT * from suidev_space')
        return self.cur.fetchall()

class VisualData(SqlConnector) :
    def __init__(self) :
        super(VisualData, self).__init__()

    def __del__(self) :
        super(VisualData, self).__del__()

    def AddPlanet(self, kind, ring, server_name) :
        insert_cmd = "INSERT INTO suidev_planet (name, create_time, kind, ring, server_name) VALUE(%s, %s, %s, %s, %s)"
        insert_data = ("", datetime.now(), kind, ring, server_name)
        self.cur.execute(insert_cmd, insert_data)
        return self.cur.lastrowid

    def AddPlanetVisual(self, planet_id, width, height, sample, fps, length, frame, format, render_time, rotate, light_angle) :
        insert_cmd = "INSERT INTO suidev_planet_visual (create_time, planet_id, width, height, sample, fps, length, frame, format, render_time, rotate_x, rotate_y, rotate_z, light_angle) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_data = (datetime.now(), planet_id,  width, height, sample, fps, length, frame, format, render_time, rotate[0], rotate[1], rotate[2], light_angle)
        self.cur.execute(insert_cmd, insert_data)
        return self.cur.lastrowid


    def GetPlanets(self, page_id, page_size):
        self.cur.execute('SELECT SQL_CALC_FOUND_ROWS * from suidev_planet  ORDER BY V.create_time DESC LIMIT 12')
        data = self.cur.fetchall()
        self.cur.execute('SELECT FOUND_ROWS() AS total')
        count = self.cur.fetchone()
        return data, count['total'] / page_size

    def GetPlanetVisuals(self, page_id, page_size):
        self.cur.execute("SELECT SQL_CALC_FOUND_ROWS P.id AS planet_id, P.create_time, P.kind, V.id AS visual_id, (SELECT SUM(render_time) FROM suidev_planet_visual  WHERE planet_id = P.id) AS render_time from suidev_planet_visual AS V join suidev_planet AS P on V.light_angle = 0 and V.format = 'PNG' and V.planet_id = P.id ORDER BY V.create_time DESC")
        data = self.cur.fetchall()
        self.cur.execute('SELECT FOUND_ROWS() AS total')
        count = self.cur.fetchone()
        return data, count['total'] / page_size

    def GetPlanetDetail(self, planet_id) :
        insert_cmd = "SELECT V.id AS visual_id FROM suidev_planet_visual AS V JOIN suidev_planet AS P on P.id=%s AND V.format = %s AND V.planet_id = P.id ORDER BY V.rotate_z ASC"
        insert_data = (planet_id, 'PNG')
        self.cur.execute(insert_cmd, insert_data)
        return self.cur.fetchall();

    def AddMaterial(self, name, color, kind, server_name):
        rgba = BlenderImporter.Color.RGBA_to_Hex(color)
        insert_cmd = "INSERT INTO suidev_material (name, create_time, color, kind) VALUE(%s, %s, %s, %s, %s)"
        insert_data = (name, datetime.now(), rgba, kind, server_name)
        self.cur.execute(insert_cmd, insert_data)
        return self.cur.lastrowid

    def AddMaterialVisual(self, material_id, width, height, file_format, sample, render_time, model, scene) :
        insert_cmd = "INSERT INTO suidev_material_visual (material_id, create_time, format, width, height, sample, render_time,  model, scene) VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_data = (material_id, datetime.now(), file_format, width, height, sample, render_time, model, scene)
        self.cur.execute(insert_cmd, insert_data)
        return self.cur.lastrowid

    def GetMaterialVisuals(self, page_id, page_size):
        self.cur.execute('SELECT SQL_CALC_FOUND_ROWS * from suidev_material_visual AS V join suidev_material AS M on V.material_id = M.id ORDER BY V.create_time DESC LIMIT ' + str(page_id * page_size) + ',' +  str(page_size))
        data = self.cur.fetchall()
        self.cur.execute('SELECT FOUND_ROWS() AS total')
        count = self.cur.fetchone()
        return data, count['total'] / page_size


class LogData(SqlConnector) :
    def __init__(self):
        super(LogData, self).__init__()

    def GetLog(self, page_id, page_size) :
        material = "SELECT SQL_CALC_FOUND_ROWS M.id, kind AS name, 'Material' AS category, 1 AS image, 0 AS video, M.create_time, server_name FROM  suidev_material_visual AS V join suidev_material AS M on V.material_id = M.id"
        planet = "SELECT id, kind AS name, 'Planet' AS category, 12 AS image, 1 AS video, create_time, server_name FROM suidev_planet"
        insert_cmd = material + " UNION ALL " + planet + " ORDER BY create_time DESC LIMIT " + str(page_id * page_size) + ',' + str(page_size)
        self.cur.execute(insert_cmd)
        data = self.cur.fetchall()
        self.cur.execute('SELECT FOUND_ROWS() AS total')
        count = self.cur.fetchone()
        return data, count['total'] / page_size

    def GetNewest(self, day) :
        material = "SELECT M.id, kind AS name, 'Material' AS category, M.create_time, V.render_time, server_name FROM  suidev_material_visual AS V join suidev_material AS M on V.material_id = M.id"
        planet = "SELECT P.id, kind AS name, 'Planet' AS category, P.create_time,  (SELECT SUM(render_time) FROM suidev_planet_visual  WHERE planet_id = P.id) AS render_time, server_name FROM suidev_planet AS P LEFT JOIN suidev_planet_visual AS PV on PV.planet_id = P.id and PV.light_angle = 0 and PV.format = 'PNG'"
        insert_cmd = "SELECT * FROM(" + material + " UNION ALL " + planet + ")N WHERE DateDiff(create_time, NOW())<=" + str(day) + " ORDER BY create_time ASC"
        self.cur.execute(insert_cmd)
        data = self.cur.fetchall()
        self.cur.execute('SELECT FOUND_ROWS() AS total')
        count = self.cur.fetchone()
        return data


class TaskData(SqlConnector) :
    def __init__(self) :
        super(TaskData, self).__init__()

    def GetTasks(self, kind) :
        select_cmd = "SELECT * FROM suidev_task WHERE kind = %(kind)s"
        select_data = {'kind': kind}
        self.cur.execute(select_cmd, select_data)
        return self.cur.fetchall()

    def SetTasks(self, tasks) :
        update_cmd = "UPDATE suidev_task SET priority = %(priority)s where name = %(name)s"
        for t in tasks :
            print(t)
            update_data = {'name' : t["name"], 'priority' : t["priority"]}
            self.cur.execute(update_cmd, update_data)
