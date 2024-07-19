import DB_handler
import cherrypy
import json
import time
import MyMQTT

def msg_handler(paho_mqtt , userdata, msg):

    data = json.loads(msg.payload.decode())
    if not 'deviceID' in data:
       return
    
    if not DB_handler.deviceRegistered(data['deviceID']):
        if not 'endpoints' in data or not 'resources' in data:
            client.mqtt.myPublish("/tiot/group6/catalog/subscription/devices/%s" % data['deviceID'], "Couldn't subscribe device: endpoints or resources field missing in request")
            return
            
        if not DB_handler.addDevice(data['deviceID'], data['endpoints'], data['resources'], time.time()):
            client.mqtt.myPublish("/tiot/group6/catalog/subscription/devices/%s" % data['deviceID'], "Couldn't subscribe device")
            return
            
        client.mqtt.myPublish("/tiot/group6/catalog/subscription/devices/%s" % data['deviceID'], "Device subscribed successfully")
    else:
        if not DB_handler.updateDevice(data['deviceID'], time.time()):
            client.mqtt.myPublish("/tiot/group6/catalog/subscription/devices/%s" % data['deviceID'], "Couldn't update device")
            return
        
        client.mqtt.myPublish("/tiot/group6/catalog/subscription/devices/%s" % data['deviceID'], "Device updated successfully")

    

class subscribe_device():
    exposed = True
    def PUT(self, *uri, **params):
        raw_body = cherrypy.request.body.read()
        body = json.loads(raw_body) 
        if not 'deviceID' in body:
            raise cherrypy.HTTPError(400, "Bad request")
        
        if not DB_handler.deviceRegistered(body['deviceID']):
            if not 'endpoints' in body or not 'resources' in body:
                raise cherrypy.HTTPError(400, "Invalid arguments")
            
            if not DB_handler.addDevice(body['deviceID'], body['endpoints'], body['resources'], time.time()):
                raise cherrypy.HTTPError(500, "Couldn't register device")
            
        else:
            if not DB_handler.updateDevice(body['deviceID'], time.time()):
                raise cherrypy.HTTPError(500, "Couldn't update device")

class get_devices():
    exposed = True
    def GET(self, *uri, **params):
        if len(uri) == 1:
            return DB_handler.getDevice(uri[0])
        
        if(len(uri) == 0):
            return DB_handler.getDevices()
        
        raise cherrypy.HTTPError(400, "wrong number of arguments")
    
class add_user():
    exposed = True
    def POST(self, *uri, **params):
        raw_body = cherrypy.request.body.read()
        body = json.loads(raw_body)
        if not ('email' in body) or not ('name' in body) or not ('surname' in body):
            raise cherrypy.HTTPError(400, "Bad request")

        if not DB_handler.addUser(body['email'], body['name'], body['surname']):
            raise cherrypy.HTTPError(500, "Errore durante la registrazione")
        
class get_users():
    exposed = True
    def GET(self, *uri, **params):
        if(len(uri) == 0):
            return DB_handler.getUsers()
            
        if(len(uri) == 1):
            return DB_handler.getUser(uri[0])
        
        raise cherrypy.HTTPError(400, "Too many arguments")

class subscribe_service():
    exposed = True
    def PUT(self, *uri, **params):
        raw_body = cherrypy.request.body.read()
        body = json.loads(raw_body)
        if not 'serviceID' in body:
            raise cherrypy.HTTPError(400, "Bad request")
        
        if not DB_handler.serviceRegistered(body['serviceID']):
            if not 'endpoints' in body or not 'description' in body:
                raise cherrypy.HTTPError(400, "Invalid arguments")
            
            if not DB_handler.addService(body['serviceID'], time.time(), body['description'], body['endpoints']):
                raise cherrypy.HTTPError(500, "Couldn't register service")
            
        else:
            if not DB_handler.updateService(body['serviceID'], time.time()):
                raise cherrypy.HTTPError(500, "Couldn't update service")


class subscription_info():
    exposed = True
    def GET(self, *uri, **params):
        output = {
            'user_subscription': {
                'REST':{
                    'path': '/subscribe/user',
                    'fields': ['name', 'surname', 'email']
                }
            },
            'device_subscription':{
                'REST':{
                    'path': '/subscribe/device',
                    'fields': ['deviceID', 'endpoints(endpoint, type(MQTT/REST))[]', 'resources(resource_name)[]']
                },
                'MQTT':{
                    'topic': '/tiot/group6/catalog/subscription/devices',
                    'fields': ['deviceID', 'endpoints(endpoint, type(MQTT/REST))[]', 'resources(resource_name)[]']
                }
            },
            'service_subscription': {
                'REST':{
                    'path': '/subscribe/service',
                    'fields': ['serviceID', 'description', 'endpoints(endpoint, type(MQTT/REST))[]']
                }
            }
        }
        return json.dumps(output)


if __name__ == '__main__':
    client = MyMQTT.Client("catalog_tiot6_polito")
    client.mqtt._paho_mqtt.on_message = msg_handler
    client.run()
    client.mqtt.mySubscribe('/tiot/group6/catalog/subscription/devices')

    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':True
        }
    }
    cherrypy.tree.mount(subscribe_device(),'/subscribe/device', conf)
    cherrypy.tree.mount(get_devices(),'/devices', conf)
    cherrypy.tree.mount(add_user(), '/subscribe/user', conf)
    cherrypy.tree.mount(get_users(), '/users', conf)
    cherrypy.tree.mount(subscribe_service(), '/subscribe/service', conf)
    cherrypy.tree.mount(subscription_info(), '/subscribe', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.engine.start()

    while(1):
        time.sleep(60)
        DB_handler.purge()
    
    cherrypy.engine.block()