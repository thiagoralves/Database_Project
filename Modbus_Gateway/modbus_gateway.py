#!/usr/bin/python

import sqlite3
from sqlite3 import Error
from pyModbusTCP.client import ModbusClient
from time import strftime 
from datetime import datetime
import time

""" Create a connection to the database file """
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return None

""" Example query """
def get_devices(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT devID FROM device WHERE deleted = 0")
        rows = cur.fetchall()
        cur.close()
        
        devices = []
        for row in rows:
            devices.append(row[0])
        return devices
        
    except Error as e:
        print(e)
    
    return None

def get_points(conn, devices):
    for device in devices:
        try:
            cur = conn.cursor()
            #Get IP Address and port from database
            cur.execute("SELECT ip, port FROM device WHERE devID = ?", (device,))
            request = cur.fetchone()
            ip = request[0]
            port = request[1]
            
            client = ModbusClient()
            client.host(ip)
            client.port(port)
            
            client_connected = True
            if (client.is_open() == False):
                if (client.open() == False):
                    print("Unable to connect to " + ip + ":" + str(port))
                    client_connected = False
                    
            if (client_connected == True):
                cur.execute("SELECT name, address, type, pointID, mult_factor FROM device_points WHERE devID = ? AND deleted = 0", (device,))
                rows = cur.fetchall()
                
                for row in rows:
                    if (row[2] == "dig_in"):
                        req = client.read_discrete_inputs(int(row[1]), 1)
                        
                        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        point_ID = row[3]
                        value = req[0]*row[4]
                        print(datetime_str + " | " + str(point_ID) + " | " + str(value))
                        cur.execute("INSERT INTO point_data VALUES (?, ?, ?)", (datetime_str, point_ID, value))
                        #print("Value for point " + row[0] + ": " + str(req) + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                        
                    if (row[2] == "dig_out"):
                        req = client.read_coils(int(row[1]), 1)
                        
                        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        point_ID = row[3]
                        value = req[0]*row[4]
                        error_code = 0
                        print(datetime_str + " | " + str(point_ID) + " | " + str(value))
                        cur.execute("INSERT INTO point_data VALUES (?, ?, ?)", (datetime_str, point_ID, value))
                        #print("Value for point " + row[0] + ": " + str(req) + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                        
                    if (row[2] == "an_in"):
                        req = client.read_input_registers(int(row[1]), 1)
                        
                        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        point_ID = row[3]
                        value = req[0]*row[4]
                        error_code = 0
                        print(datetime_str + " | " + str(point_ID) + " | " + str(value))
                        cur.execute("INSERT INTO point_data VALUES (?, ?, ?)", (datetime_str, point_ID, value))
                        #print("Value for point " + row[0] + ": " + str(req) + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                        
                    if (row[2] == "an_out"):
                        req = client.read_holding_registers(int(row[1]), 1)
                        
                        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        point_ID = row[3]
                        value = req[0]*row[4]
                        error_code = 0
                        print(datetime_str + " | " + str(point_ID) + " | " + str(value))
                        cur.execute("INSERT INTO point_data VALUES (?, ?, ?)", (datetime_str, point_ID, value))
                        #print("Value for point " + row[0] + ": " + str(req) + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            
                print("\n")
                conn.commit()
                cur.close()
                client.close()
            
        except Error as e:
            print(e)
            conn.close()
            database = "./database/SCADADB.db"
            conn = create_connection(database)

def main():
    print("Connecting to the database...")
    
    database = "./database/SCADADB.db"
    conn = create_connection(database)
    
    if (conn != None):
        print("Connected!\n\n")
        
        while (True):
            devices = get_devices(conn)
            
            if (devices != None):
                get_points(conn, devices)
                
            else:
                database = "./database/SCADADB.db"
                conn = create_connection(database)
            
            time.sleep(0.1)
            
    else:
        print("Error connecting to the database!")
    
    
if __name__ == '__main__':
    main()