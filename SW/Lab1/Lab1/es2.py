
import cherrypy
import json

def convert(original, target, value):
    try:
        val = float(value)
    except ValueError as ve:
        raise cherrypy.HTTPError(400, "Value to convert is not a number")
    
    if original == "C":
        if target == "K":
            return val + 273.15
        if target == "F":
            return val * 9/5 + 32
        return val
    
    if original == "K":
        if target == "C":
            return val - 273.15
        if target == "F":
            return (val - 273.15) * 9/5 + 32
        return val
    
    if original == "F":
        if target == "C":
            return (val - 32) * 5/9
        if target == "K":
            return (val + 459.67) * 5/9
        return val

class MyWebService(object):
    exposed = True
    def GET(self, *uri, **params):
        
        if len(uri) != 3:
            raise cherrypy.HTTPError(400, "Invalid number of arguments")

        if uri[1] != "C" and uri[1] != "F" and uri[1] != "K":
            raise cherrypy.HTTPError(400, "Invalid original unit of measurement")
        
        if uri[2] != "C" and uri[2] != "F" and uri[2] != "K":
            raise cherrypy.HTTPError(400, "Invalid target unit of measurement")
        
        converted_value = round(convert(uri[1], uri[2], uri[0]), 2)
        return json.dumps({
            "original value":uri[0], 
            "original":uri[1], 
            "converted value":converted_value, 
            "target":uri[2]
        })


if __name__ == '__main__':
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':True
        }
    }
    cherrypy.tree.mount(MyWebService(),'/converter',conf)
    cherrypy.engine.start()
    cherrypy.engine.block()