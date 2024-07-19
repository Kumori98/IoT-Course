import requests
import time
import MyMQTT

ip = "http://192.168.1.14:8080/"

def main():
    endpoints = [{"endpoint" : "prova1",  "type" : "MQTT"}, {"endpoint" : "prova2", "type" : "REST"}]
    resources = ["temperature", "humidity"]

    user1 = { "name" : "Giovanni", "surname" : "Pizzenti", "email" : "giannipizzeni@gmail.com"}
    user2 = { "name" : "Marco", "surname" : "Pizzenti", "email" : "marcopizzenti@gmail.com"}
    device  = { "deviceID" : "device6", "endpoints" : endpoints,  "resources" : resources}
    service = {"serviceID" : "service6", "description" : "descrizione", "endpoints" : endpoints}

    response = requests.post(ip + "subscribe/user", json = user1)
    print("user 1:")
    print(response)

    response = requests.post(ip + "subscribe/user", json = user2)
    print("user 2:")
    print(response)

    #richiedi tutti gli utenti
    response = requests.get( ip + "/users/")
    print("users:")
    print(response.content)

    #richiedi un servizio
    reponse = requests.get(ip + "/service/" + serviceID)
    print("service:")
    print(reponse.content)

    #richiedi un dispositivo
    response = requests.get(ip + "devices")
    print("devices:")
    print(response.content)

    while(1) :
        response = requests.put( ip + "subscribe/device" ,  json = device)
        print(response)
        response = requests.put(ip + "subscribe/service", json = service)
        print(response)
        time.sleep(10)





if __name__ == "__main__":
    main()