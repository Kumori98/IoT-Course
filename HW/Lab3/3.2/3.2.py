import cherrypy
import json
import sqlite3

def storeData(data):
    conn = sqlite3.connect("DB.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO Temperature (v, t) VALUES(?, ?)"
        cursor.execute(sql, (data['v'], data['t']))
        conn.commit()
        success = True
    except:
        conn.rollback()
        success = False
    
    cursor.close()
    conn.close()
    return success
    
def retrieveData():
    conn = sqlite3.connect("DB.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Temperature"
    cursor.execute(sql, ())
    output = cursor.fetchall()

    cursor.close()
    conn.close()
    return json.dumps( [dict(ix) for ix in output] )

class MyWebService(object):
    exposed = True
    def POST(self, *uri, **params):
        input = cherrypy.request.body.read()
        js = json.loads(input)
        if not storeData(js['e'][0]):
            raise cherrypy.HTTPError(500, "Errore")

    def GET(self, *uri, **params):
        return retrieveData()


if __name__ == '__main__':
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':False
        }
    }
    cherrypy.tree.mount(MyWebService(),'/log',conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.engine.start()
    cherrypy.engine.block()
