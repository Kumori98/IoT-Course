import sqlite3
import json
import time

def addDevice(id, endpoints, resources, timestamp):
    conn = sqlite3.connect("catalog.db")
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO Devices(ID, insert_timestamp) VALUES (?, ?)"
        cursor.execute(sql, (id, int(timestamp)))

        sql = "INSERT INTO DeviceEndpoints (device, endpoint, type) VALUES (?, ?, ?)"
        for endpoint in endpoints:
            cursor.execute(sql, (id, endpoint['endpoint'], endpoint['type']))

        sql = "INSERT INTO Resources (device, resource) VALUES (?, ?)"
        for resource in resources:
            cursor.execute(sql, (id, resource))
        
        conn.commit()
        success = True

    except Exception as e:
        print(e)
        conn.rollback()   
        success = False
   
    cursor.close()
    conn.close()
    return success

def getResources(device):
    conn = sqlite3.connect("Catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT resource FROM Resources WHERE device = ?"
    cursor.execute(sql, (device, ))
    output = cursor.fetchall()

    cursor.close()
    conn.close()
    return [dict(row) for row in output]

def remDevice(deviceID):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql1 = "DELETE FROM Resources WHERE device = ?"
    sql2 = "DELETE FROM DeviceEndpoints WHERE device = ?"
    sql3 = "DELETE FROM Devices WHERE ID = ?"
    try:
        cursor.execute(sql1, (deviceID, ))
        cursor.execute(sql2, (deviceID, ))
        cursor.execute(sql3, (deviceID, ))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()
        success = False

    cursor.close()
    conn.close()
    return success
    
def getDevEndpoints(deviceID):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM DeviceEndpoints WHERE device = ?"
    cursor.execute(sql, (deviceID, ))
    output = cursor.fetchall()

    cursor.close()
    conn.close()
    return [dict(row) for row in output]
    

def getDevices():
    output = {'devices':[]}
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = "SELECT * FROM Devices"
    cursor.execute(sql, ())
    devices = cursor.fetchall()

    for dev in devices:
        dict = {"id": dev['ID'], "insert_timestamp": dev['insert_timestamp']}
        dict['resources'] = getResources(dev['ID'])
        dict['endpoints'] = getDevEndpoints(dev['ID'])
        output['devices'].append(dict)

    cursor.close()
    conn.close()
    return json.dumps(output)


def getDevice(id):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Devices WHERE ID = ?"
    cursor.execute(sql, (id, ))
    dev_raw = cursor.fetchone()

    output = {"id": id, "insert_timestamp": dev_raw['insert_timestamp']}
    output['resources'] = getResources(id)
    output['endpoints'] = getDevEndpoints(id)

    cursor.close()
    conn.close()
    return json.dumps(output)

def addUser(email, name, surname):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "INSERT INTO Users(email, name, surname) VALUES(?, ?, ?)"
    try:
        cursor.execute(sql, (email, name, surname))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()
        success = False

    cursor.close()
    conn.close()
    return success

def getUser(email):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Users WHERE email = ?"
    cursor.execute(sql, (email, ))
    output = cursor.fetchone()

    cursor.close()
    conn.close()
    return json.dumps({
        'name': output['name'],
        'surname': output['surname'],
        'email': output['email']
    })

def getUsers():
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Users"
    cursor.execute(sql, ())
    output = cursor.fetchall()

    cursor.close()
    conn.close()
    return json.dumps([dict(row) for row in output])

def deviceRegistered(devID):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Devices WHERE ID = ?"
    cursor.execute(sql, (devID, ))
    count = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return len(count)

def updateDevice(devID, time):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "UPDATE Devices SET insert_timestamp = ? WHERE ID = ?"
    try:
        cursor.execute(sql, (time, devID))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()
        success = False

    cursor.close()
    conn.close()
    return success

def addServiceEP(endpoint):
    conn = sqlite3.connect("catalog.db")
    cursor = conn.cursor()

    sql = "INSERT INTO ServiceEndpoints(service, endpoint, type) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (endpoint['service'], endpoint['endpoint'], endpoint['type']))
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        success = False
    
    cursor.close()
    conn.close()
    return success

def addService(id, time, description, endpoints):
    conn = sqlite3.connect("catalog.db")
    cursor = conn.cursor()

    sql = "INSERT INTO Services(ID, insert_timestamp, description) VALUES (?, ?, ?)"
    try:
        cursor.execute(sql, (id, time, description))

        sql = "INSERT INTO ServiceEndpoints(service, endpoint, type) VALUES (?, ?, ?)"
        for endpoint in endpoints:
            cursor.execute(sql, (id, endpoint['endpoint'], endpoint['type']))

        conn.commit()
        success = True

    except Exception as e:
        print(e)
        conn.rollback()
        success = False

    cursor.close()
    conn.close()
    return success

def serviceRegistered(servID):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Services WHERE ID = ?"
    cursor.execute(sql, (servID, ))
    count = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return len(count)

def updateService(servID, time):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "UPDATE Services SET insert_timestamp = ? WHERE ID = ?"
    try:
        cursor.execute(sql, (time, servID))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()
        success = False

    cursor.close()
    conn.close()
    return success

def remService(serviceID):
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql1 = "DELETE FROM ServiceEndpoints WHERE service = ?"
    sql2 = "DELETE FROM Services WHERE ID = ?"
    try:
        cursor.execute(sql1, (serviceID, ))
        cursor.execute(sql2, (serviceID, ))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        conn.rollback()
        success = False

    cursor.close()
    conn.close()
    return success

def purge():
    conn = sqlite3.connect("catalog.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    now = time.time()
    
    sql = "SELECT ID FROM Devices WHERE (? - insert_timestamp > 20)"
    cursor.execute(sql, (now, ))
    devices = cursor.fetchall()

    for dev in devices:
        remDevice(dev['ID'])

    sql = "SELECT ID FROM Services WHERE (? - insert_timestamp > 20)"
    cursor.execute(sql, (now, ))
    services = cursor.fetchall()

    for service in services:
        remService(service['ID'])

    cursor.close()
    conn.close()