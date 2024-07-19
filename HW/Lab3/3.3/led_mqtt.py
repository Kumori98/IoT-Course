import MyMQTT


def main():
    client = MyMQTT.Client("LedSwitch")
    client.run()
    client.mqtt.mySubscribe("/tiot/group6/temperature")
    
    user_in = input("")
    while user_in != "-1":

        if user_in != "0" and user_in != "1" and user_in != "-1":
            print("comando non valido")
            continue

        msg = '{"bn": "ArduinoGroup6", "e":[{"n": "led", "t": null, "v": %s, "u": null}]}' % user_in
        client.mqtt.myPublish("/tiot/group6/led", msg)
        print("Mandato")

        user_in = input("")

    client.end()
    print("Fine")
    

if __name__ == "__main__":
    main()