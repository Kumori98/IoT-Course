import MyMQTT
import time

if __name__ == '__main__':
    client = MyMQTT.Client("MQTTdevice_tiot6")
    client.run()
    client.mqtt.mySubscribe('/tiot/group6/catalog/subscription/devices/MQTTdevice_tiot6')
    time.sleep(5)
    while(1):
        client.mqtt.myPublish('/tiot/group6/catalog/subscription/devices', '{ "deviceID": "MQTTdevice_tiot6", "endpoints" : [{"endpoint": "localhost", "type": "REST"}],  "resources" : ["humidity", "height"]}')
        time.sleep(30)