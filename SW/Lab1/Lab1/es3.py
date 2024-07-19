
import cherrypy
import json
import time

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
    
def convert_rounded(original, target, value):
    return round(convert(original, target, value), 2)

class MyWebService(object):
    exposed = True
    def POST(self, *uri, **params):

        body = cherrypy.request.body.read()
        input = json.loads(body)

        if len(input.keys()) > 3:
            raise cherrypy.HTTPError(400, "Invalid number of arguments")
        
        if input["originalUnit"] != "C" and input["originalUnit"] != "F" and input["originalUnit"] != "K":
            raise cherrypy.HTTPError(400, "Invalid original unit of measurement")
        
        if input["targetUnit"] != "C" and input["targetUnit"] != "F" and input["targetUnit"] != "K":
            raise cherrypy.HTTPError(400, "Invalid target unit of measurement")
        
        converted_values = list(map(lambda val: convert_rounded(input["originalUnit"], input["targetUnit"], val), input["values"]))

        output = json.dumps({
            "values":input["values"],
            "targetValues":converted_values,
            "originalUnit":input["originalUnit"],
            "targetUnit":input["targetUnit"],
            "timestamp":round(time.time(), 3)
        })
        
        return output

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