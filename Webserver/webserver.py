import sqlite3
from sqlite3 import Error
from time import strftime 
from datetime import datetime
import time
import pages

from flask import Flask, request
app = Flask(__name__)

#----------------------------------------------------------------------------
#The home page is the login page.
#----------------------------------------------------------------------------
@app.route('/')
def login():
   return pages.login_page

#----------------------------------------------------------------------------
#Intermediary page to check the login. If valid, redirects to the 
#devices page with the user logged in.
#----------------------------------------------------------------------------
@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
   #If the method is GET, reject the request and return to the login page
   if request.method == 'GET':
      return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/"></head></html>'
   else:
      user_name = request.form['uname']
      password = request.form['psw']
      
      database = "../SCADADB.db"
      conn = create_connection(database)
      if (conn != None):
         try:
            cur = conn.cursor()
            cur.execute("SELECT email, password FROM user")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            should_login = False
            for row in rows:
               if (row[0] == user_name and row[1] == password):
                  should_login = True
                  
            if (should_login == True):
               #Redirect to the devices page
               return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/devices"></head></html>'
            else:
               #Display wrong user/pass error page
               return '<!DOCTYPE html><html><h1>Wrong User Name or Password!</h1></html>'
            
         except Error as e:
            return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
      
      return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#Devices page. Here the user can see a list of devices registered on the 
#database. It is possible to add a new device to the database or edit an 
#existing device.
#----------------------------------------------------------------------------
@app.route('/devices')
def devices():
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.device_page_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT * FROM device WHERE deleted = 0")
         rows = cur.fetchall()

         for row in rows:
            cur2 = conn.cursor()
            cur2.execute("SELECT Loc_Name FROM Locations WHERE lid = ?", (row[5],))
            location = cur2.fetchone()
            return_str += "<tr onclick=\"document.location='/edit_device?dev_id=" + str(row[0]) + '\'"><td>' + str(row[4]) + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td><td>' + str(location[0]) + '</td></tr>'
         
         cur.close()
         cur2.close()
         conn.close()
         return_str += '</table><br><br><div style="text-align:center"><form method="POST" action="/add_device"><input type="submit" value="Insert New Device"></form></div></div></body></html>'

      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving devices'

   return return_str

#----------------------------------------------------------------------------
#This page allows the user to insert a new device on the database.
#----------------------------------------------------------------------------
@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.add_device_page
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT Loc_Name FROM Locations")
         rows = cur.fetchall()
         for row in rows:
            return_str += "<option value='" + str(row[0]) + "'>" + str(row[0]) + "</option>"
            
         return_str += (   "</select>"
                           "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                       )
                       
      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving points'
   
   return return_str

#----------------------------------------------------------------------------
#This page allows the user to update a device on the database.
#----------------------------------------------------------------------------
@app.route('/edit_device', methods=['GET', 'POST'])
def edit_device():
   dev_id = request.args.get('dev_id')
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.default_pages_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT * FROM device WHERE devID = ?", (int(dev_id),))
         row = cur.fetchone()
         cur2 = conn.cursor()
         cur2.execute("SELECT lid, Loc_Name FROM Locations")
         locations = cur2.fetchall()
         cur.close()
         cur2.close()
         conn.close()
         
         return_str += ("<h2>Edit Device</h2>"
                        "<form action='/edit_device_action?dev_id=" + dev_id + "' method='post'>"
                            "<label for='devname'>Device Name</label>"
                       )
         return_str += "<input type='text' id='devname' name='dev_name' value='" + str(row[4]) + "'>"
         return_str += "<label for='ip'>IP</label>"
         return_str += "<input type='text' id='ip' name='dev_ip' value='" + str(row[1]) + "'>"
         return_str += "<label for='port'>Port</label>"
         return_str += "<input type='text' id='port' name='dev_port' value='" + str(row[2]) + "'>"
         return_str += "<label for='locName'>Location</label>"
         return_str += "<select id='locName' name='loc_name'>"
         
         for location in locations:
            if (location[0] == row[5]):
               return_str += "<option value='" + str(location[1]) + "' selected='selected'>" + str(location[1]) + "</option>"
            else:
               return_str += "<option value='" + str(location[1]) + "'>" + str(location[1]) + "</option>"
         
         return_str += (    "</select>"
                            "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "<button type=\"button\" style=\"background-color:FireBrick\" onclick=\"location.href='delete_device?dev_id=" + dev_id + "';\">Delete</button>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                      )
                      
         return return_str
         
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
   
   else:
      return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page executes the insertion on the database.
#----------------------------------------------------------------------------
@app.route('/add_device_action', methods=['GET', 'POST'])
def add_device_action():
   dev_name = request.form['dev_name']
   dev_ip = request.form['dev_ip']
   dev_port = request.form['dev_port']
   loc_name = request.form['loc_name']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT lid FROM Locations WHERE Loc_Name = ?", (loc_name,))
         lid = cur.fetchone()
         
         cur2 = conn.cursor()
         cur2.execute("INSERT INTO device (DeviceName, IP, port, deleted, LocID) VALUES (?, ?, ?, 0, ?)", (dev_name, dev_ip, int(dev_port), lid[0]))
         conn.commit()
         cur.close()
         cur2.close()
         conn.close()
         
         #Redirect back to the devices page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/devices"></head></html>'
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'
   
#----------------------------------------------------------------------------
#This page executes the update query on the database.
#----------------------------------------------------------------------------
@app.route('/edit_device_action', methods=['GET', 'POST'])
def edit_device_action():
   dev_id = request.args.get('dev_id')
   dev_name = request.form['dev_name']
   dev_ip = request.form['dev_ip']
   dev_port = request.form['dev_port']
   loc_name = request.form['loc_name']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT lid FROM Locations WHERE Loc_Name = ?", (loc_name,))
         lid = cur.fetchone()
         
         cur2 = conn.cursor()
         cur2.execute("UPDATE device SET DeviceName = ?, IP = ?, port = ?, LocID = ? WHERE devID = ?", (dev_name, dev_ip, int(dev_port), lid[0], int(dev_id)))
         conn.commit()
         cur.close()
         cur2.close()
         conn.close()
         
         #Redirect back to the devices page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/devices"></head></html>'
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'
   
#----------------------------------------------------------------------------
#This page "deletes" a device on the database. The deletion in this case
#is actually just a flag that is set.
#----------------------------------------------------------------------------
@app.route('/delete_device', methods=['GET', 'POST'])
def delete_device():
   dev_id = request.args.get('dev_id')
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("UPDATE device SET deleted = 1 WHERE devID = ?", (int(dev_id),))
         conn.commit()
         cur.close()
         conn.close()
         
         #Redirect back to the devices page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/devices"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'
   
#----------------------------------------------------------------------------
#Points page. This page is used to verify information about each PLC point.
#The user can edit a point or create a new one and associate it with any of
#the PLCs registered on the database.
#----------------------------------------------------------------------------
@app.route('/points', methods=['GET', 'POST'])
def points():
   filter_by = dev_id = request.args.get('filter_by')
   if (filter_by == None):
      filter_by = "All"
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.point_page_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT DeviceName FROM device WHERE deleted = 0")
         rows = cur.fetchall()
         for row in rows:
            if (str(row[0]) == filter_by):
               return_str += "<option value='" + str(row[0]) + "' selected='selected'>" + str(row[0]) + "</option>"
            else:
               return_str += "<option value='" + str(row[0]) + "'>" + str(row[0]) + "</option>"
            
         return_str += "</select></h3>"
         
         return_str += (  "<table>"
                          "<tr style='background-color: white'>"
                           "<th>Point Name</th><th>Address</th><th>Type</th><th>Multiplication Factor</th><th>Description</th><th>Device</th>"
                          "</tr>"
                       )
         
         if (filter_by == "All"):
            cur.execute("SELECT p.name, p.address, p.type, p.mult_factor, p.description, p.pointID, d.DeviceName FROM Device_points p, device d WHERE p.devID = d.devID AND p.deleted = 0 AND d.deleted = 0")
         else:
            cur.execute("SELECT p.name, p.address, p.type, p.mult_factor, p.description, p.pointID, d.DeviceName FROM Device_points p, device d WHERE p.devID = d.devID AND p.deleted = 0 AND d.deleted = 0 AND d.DeviceName = ?", (filter_by,))
         rows = cur.fetchall()
         cur.close()
         conn.close()

         for row in rows:
            return_str += "<tr onclick=\"document.location='/edit_point?point_id=" + str(row[5]) + '\'"><td>' + str(row[0]) + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td><td>' + str(row[3])+ '</td><td>' + str(row[4]) + '</td><td>' + str(row[6]) + '</td></tr>'
         
         return_str += '</table><br><br><div style="text-align:center"><form method="POST" action="/add_point"><input type="submit" value="Insert New Point"></form></div></div></body></html>'

      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving points'

   return return_str
   
#----------------------------------------------------------------------------
#This page allows the user to insert a new point on the database.
#----------------------------------------------------------------------------
@app.route('/add_point', methods=['GET', 'POST'])
def add_point():
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.add_point_page
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT DeviceName FROM device WHERE deleted = 0")
         rows = cur.fetchall()
         for row in rows:
            return_str += "<option value='" + str(row[0]) + "'>" + str(row[0]) + "</option>"
            
         return_str += (   "</select>"
                           "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                       )
                       
      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving points'
   
   return return_str
                 

#----------------------------------------------------------------------------
#This page executes the insertion on the database.
#----------------------------------------------------------------------------
@app.route('/add_point_action', methods=['GET', 'POST'])
def add_point_action():
   point_name = request.form['point_name']
   point_address = request.form['point_address']
   point_type = request.form['point_type']
   mult_fact = request.form['mult_fact']
   point_description = request.form['point_description']
   dev_name = request.form['dev_name']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT devID FROM device WHERE DeviceName = ? AND deleted = 0", (dev_name,))
         dev_id = cur.fetchone()
         
         cur2 = conn.cursor()
         cur2.execute("INSERT INTO Device_points (name, address, type, description, devID, mult_factor, deleted) VALUES (?, ?, ?, ?, ?, ?, 0)", (point_name, point_address, point_type, point_description, int(dev_id[0]), float(mult_fact)))
         conn.commit()
         cur.close()
         cur2.close()
         conn.close()
         
         #Redirect back to the points page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/points"></head></html>'
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page allows the user to update a device on the database.
#----------------------------------------------------------------------------
@app.route('/edit_point', methods=['GET', 'POST'])
def edit_point():
   point_id = request.args.get('point_id')
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.default_pages_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT * FROM Device_points WHERE pointID = ?", (int(point_id),))
         row = cur.fetchone()
         cur2 = conn.cursor()
         cur2.execute("SELECT DeviceName, devID FROM device WHERE deleted = 0")
         devices = cur2.fetchall()
         cur.close()
         cur2.close()
         conn.close()
         
         return_str += ("<h2>Edit Point</h2>"
                        "<form action='/edit_point_action?point_id="+ point_id +"' method='post'>"
                            "<label for='pointName'>Point Name</label>"
                       )
         return_str += "<input type='text' id='pointName' name='point_name' value='" + str(row[0]) + "'>"
         return_str += "<label for='pointAddress'>Address</label>"
         return_str += "<input type='text' id='pointAddress' name='point_address' value='" + str(row[1]) + "'>"
         return_str += "<label for='pointType'>Type</label>"
         
         return_str += "<select id='pointType' name='point_type'>"
         if (str(row[2]) == "dig_in"):
            return_str += "<option value='dig_in' selected='selected'>dig_in</option>"
         else:
            return_str += "<option value='dig_in'>dig_in</option>"
         
         if (str(row[2]) == "dig_out"):
            return_str += "<option value='dig_out' selected='selected'>dig_out</option>"
         else:
            return_str += "<option value='dig_out'>dig_out</option>"
         
         if (str(row[2]) == "an_in"):
            return_str += "<option value='an_in' selected='selected'>an_in</option>"
         else:
            return_str += "<option value='an_in'>an_in</option>"
         
         if (str(row[2]) == "an_out"):
            return_str += "<option value='an_out' selected='selected'>an_out</option>"
         else:
            return_str += "<option value='an_out'>an_out</option>"
         return_str += "</select>"
         
         return_str += "<label for='multFact'>Multiplication Factor</label>"
         return_str += "<input type='text' id='multFact' name='mult_fact' value='" + str(row[6]) + "'>" 
         return_str += "<label for='pointDescription'>Description</label>"
         return_str += "<input type='text' id='pointDescription' name='point_description' value='" + str(row[3]) + "'>" 
         return_str += "<label for='devName'>Device</label>"
         return_str += "<select id='devName' name='dev_name'>"
         
         for device in devices:
            if (device[1] == row[4]):
               return_str += "<option value='" + str(device[0]) + "' selected='selected'>" + str(device[0]) + "</option>"
            else:
               return_str += "<option value='" + str(device[0]) + "'>" + str(device[0]) + "</option>"

         return_str += (    "</select>"
                            "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "<button type=\"button\" style=\"background-color:FireBrick\" onclick=\"location.href='delete_point?point_id=" + point_id + "';\">Delete</button>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                      )
                      
         return return_str
         
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
   
   else:
      return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page executes the update query on the database.
#----------------------------------------------------------------------------
@app.route('/edit_point_action', methods=['GET', 'POST'])
def edit_point_action():
   point_id = request.args.get('point_id')
   
   point_name = request.form['point_name']
   point_address = request.form['point_address']
   point_type = request.form['point_type']
   mult_fact = request.form['mult_fact']
   point_description = request.form['point_description']
   dev_name = request.form['dev_name']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT devID FROM device WHERE DeviceName = ? AND deleted = 0", (dev_name,))
         dev_id = cur.fetchone()
         
         cur2 = conn.cursor()
         cur2.execute("UPDATE Device_points SET name = ?, address = ?, type = ?, description = ?, devID = ?, mult_factor = ? WHERE pointID = ?", (point_name, point_address, point_type, point_description, int(dev_id[0]), float(mult_fact), int(point_id)))
         conn.commit()
         cur.close()
         cur2.close()
         conn.close()
         
         #Redirect back to the devices page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/points"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page "deletes" a point on the database. The deletion in this case
#is actually just a flag that is set.
#----------------------------------------------------------------------------
@app.route('/delete_point', methods=['GET', 'POST'])
def delete_point():
   point_id = request.args.get('point_id')
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("UPDATE Device_points SET deleted = 1 WHERE pointID = ?", (int(point_id),))
         conn.commit()
         cur.close()
         conn.close()
         
         #Redirect back to the points page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/points"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'
   
#----------------------------------------------------------------------------
#Data view page. On this page the user can interact with the data collected
#by each PLC point. It is possible to filter the data by PLC. All data is
#visualized in charts. Beware: This is a complicated function!
#----------------------------------------------------------------------------
@app.route('/view', methods=['GET', 'POST'])
def view():
   filter_by = dev_id = request.args.get('filter_by')
   if (filter_by == None):
      filter_by = "All"
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.view_point_header
   chart_counter = 0
   
   #Start building the header string. This string holds the JavaScript
   #functions that will draw the charts. It must be loaded before the
   #HTML code.
   header_str = ( "<!DOCTYPE html>"
                  "<html>"
                  "<head>"
                  "<meta name='viewport' content='width=device-width, user-scalable=no'>"
                  "<script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>"
                  "<script type='text/javascript'>"
                  "google.charts.load('current', {'packages':['corechart']});"
                )
   
   if (conn != None):
      try:
         #Initially we must get all the PLC devices to build the popup
         #selector on the HTML string
         cur = conn.cursor()
         cur.execute("SELECT DeviceName FROM device WHERE deleted = 0")
         rows = cur.fetchall()
         for row in rows:
            if (str(row[0]) == filter_by):
               return_str += "<option value='" + str(row[0]) + "' selected='selected'>" + str(row[0]) + "</option>"
            else:
               return_str += "<option value='" + str(row[0]) + "'>" + str(row[0]) + "</option>"
            
         return_str += "</select></h3>"
         
         #Now we need to get all the points associated with each device. If there is
         #a filter in place, we filter it here
         cur2 = conn.cursor()
         if (filter_by == "All"):
            cur2.execute("SELECT p.name, p.description, p.pointID, d.DeviceName FROM Device_points p, device d WHERE p.devID = d.devID AND p.deleted = 0 AND d.deleted = 0")
         else:
            cur2.execute("SELECT p.name, p.description, p.pointID, d.DeviceName FROM Device_points p, device d WHERE p.devID = d.devID AND p.deleted = 0 AND d.deleted = 0 AND d.DeviceName = ?", (filter_by,))
         points = cur2.fetchall()
         cur.close()
         cur2.close()
         
         for point in points:
            #Build a JavaScript function for each point in the database and 
            #statically insert all the data for each point.
            header_str += "google.charts.setOnLoadCallback(drawChart_" + str(chart_counter) + ");"
            header_str += "function drawChart_" + str(chart_counter) + "() {"
            header_str += "var data = new google.visualization.DataTable();"
            header_str += "data.addColumn('datetime', 'Time');"
            header_str += "data.addColumn('number', 'Value');"
            header_str += "data.addRows(["
            
            #For each point add a div on the HTML portion as well
            return_str += "<h3>Point: " + str(point[0]) + "</h3><p>" + str(point[1]) + "</p>"
            return_str += "<div id='" + "chart_" + str(chart_counter) + "'></div>"
            
            #Query all data for a particular PLC point and write the data
            #statically on the chart table
            cur3 = conn.cursor()
            cur3.execute("SELECT date_time, value FROM point_data WHERE point_ID = ? ORDER BY date_time DESC LIMIT 300", (int(point[2]),))
            data_points = cur3.fetchall()
            for data_point in data_points:
               header_str += "[new Date('" + str(data_point[0]) + "'), " + str(data_point[1]) + "],"
            header_str += "]);"
            
            #Write the end of the JavaScript chart function
            header_str += ("var options = {title: 'Point Visualization',"
                                          "curveType: 'function',"
                                          "legend: { position: 'right' },"
                                          "explorer: {actions: ['dragToZoom', 'rightClickToReset']},"
                                          "width:1200,"
                                          "height:600};"
                           "var chart = new google.visualization.LineChart(document.getElementById('chart_" + str(chart_counter) + "'));"
                           "chart.draw(data, options);}"
                          )
            
            chart_counter = chart_counter + 1
            
         header_str += "</script>"
         return_str += '</div></div></body></html>'

      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving points'

   return header_str + return_str

#----------------------------------------------------------------------------
#Users page. Here the user can see a list of users registered on the 
#database. It is possible to add a new user to the database, edit or delete 
#an existing user.
#----------------------------------------------------------------------------
@app.route('/users')
def users():
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.user_page_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT * FROM user")
         rows = cur.fetchall()
         cur.close()
         conn.close()

         for row in rows:
            return_str += "<tr onclick=\"document.location='/edit_user?user_id=" + str(row[4]) + '\'"><td>' + str(row[0]) + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td></tr>'
         
         return_str += '</table><br><br><div style="text-align:center"><form method="POST" action="/add_user"><input type="submit" value="Add New User"></form></div></div></body></html>'

      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving users'

   return return_str   

#----------------------------------------------------------------------------
#This page allows the user to update an user on the database.
#----------------------------------------------------------------------------
@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
   user_id = request.args.get('user_id')
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.default_pages_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT * FROM user WHERE uid = ?", (int(user_id),))
         row = cur.fetchone()
         cur.close()
         conn.close()
         
         return_str += ("<h2>Edit User</h2>"
                        "<form action='/edit_user_action?user_id=" + user_id + "' method='post'>"
                            "<label for='fname'>First Name</label>"
                       )
         return_str += "<input type='text' id='fname' name='user_fname' value='" + str(row[0]) + "'>"
         return_str += "<label for='lname'>Last Name</label>"
         return_str += "<input type='text' id='lname' name='user_lname' value='" + str(row[1]) + "'>"
         return_str += "<label for='email'>E-mail</label>"
         return_str += "<input type='text' id='email' name='user_email' value='" + str(row[2]) + "'>"
         return_str += "<label for='password'>Password</label>"
         return_str += "<input type='text' id='password' name='user_pass' value='" + str(row[3]) + "'>"
         
         return_str += (    "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "<button type=\"button\" style=\"background-color:FireBrick\" onclick=\"location.href='delete_user?user_id=" + user_id + "';\">Delete</button>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                       )
                      
         return return_str
         
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
   
   else:
      return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page executes the update query on the database.
#----------------------------------------------------------------------------
@app.route('/edit_user_action', methods=['GET', 'POST'])
def edit_user_action():
   user_id = request.args.get('user_id')
   user_fname = request.form['user_fname']
   user_lname = request.form['user_lname']
   user_email = request.form['user_email']
   user_pass = request.form['user_pass']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("UPDATE user SET fname = ?, lname = ?, email = ?, password = ? WHERE uid = ?", (user_fname, user_lname, user_email, user_pass, int(user_id)))
         conn.commit()
         cur.close()
         conn.close()
         
         #Redirect back to the users page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/users"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page allows the user to insert a new user on the database.
#----------------------------------------------------------------------------
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
   return pages.add_user_page

#----------------------------------------------------------------------------
#This page executes the insertion on the database.
#----------------------------------------------------------------------------
@app.route('/add_user_action', methods=['GET', 'POST'])
def add_user_action():
   user_fname = request.form['user_fname']
   user_lname = request.form['user_lname']
   user_email = request.form['user_email']
   user_pass = request.form['user_pass']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("INSERT INTO user (fname, lname, email, password) VALUES (?, ?, ?, ?)", (user_fname, user_lname, user_email, user_pass))
         conn.commit()
         cur.close()
         conn.close()
         
         #Redirect back to the users page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/users"></head></html>'
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page deletes a user from the database.
#----------------------------------------------------------------------------
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
   user_id = request.args.get('user_id')
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("DELETE FROM user WHERE uid = ?", (int(user_id),))
         conn.commit()
         cur.close()
         conn.close()
         
         #Redirect back to the users page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/users"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#Locations page. Here the user can see a list of locations registered on the 
#database. It is possible to add a new location to the database, edit or delete 
#an existing location.
#----------------------------------------------------------------------------
@app.route('/locations')
def locations():
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.location_page_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT l.Loc_Name, l.Address, l.Description, u.fname, u.lname, l.lid FROM Locations l, user u WHERE u.uid = l.Sup_uid")
         rows = cur.fetchall()
         cur.close()
         conn.close()

         for row in rows:
            return_str += "<tr onclick=\"document.location='/edit_location?lid=" + str(row[5]) + '\'"><td>' + str(row[0]) + '</td><td>' + str(row[1]) + '</td><td>' + str(row[2]) + '</td><td>' + str(row[3]) + ' ' + str(row[4]) + '</td></tr>'
         
         return_str += '</table><br><br><div style="text-align:center"><form method="POST" action="/add_location"><input type="submit" value="Add New Location"></form></div></div></body></html>'

      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving users'

   return return_str   

#----------------------------------------------------------------------------
#This page allows the user to update a location on the database.
#----------------------------------------------------------------------------
@app.route('/edit_location', methods=['GET', 'POST'])
def edit_location():
   lid = request.args.get('lid')
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.default_pages_header
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT * FROM Locations WHERE lid = ?", (int(lid),))
         row = cur.fetchone()
         
         return_str += ("<h2>Edit Location</h2>"
                        "<form action='/edit_location_action?lid=" + lid + "' method='post'>"
                            "<label for='lname'>Location Name</label>"
                       )
         return_str += "<input type='text' id='lname' name='loc_name' value='" + str(row[1]) + "'>"
         return_str += "<label for='address'>Address</label>"
         return_str += "<input type='text' id='address' name='loc_address' value='" + str(row[2]) + "'>"
         return_str += "<label for='descr'>Description</label>"
         return_str += "<input type='text' id='descr' name='loc_descr' value='" + str(row[3]) + "'>"
         return_str += "<label for='supervisor'>Supervisor</label>"
         return_str += "<select id='supervisor' name='loc_super'>"
         
         cur2 = conn.cursor()
         cur2.execute("SELECT fname, lname, uid FROM user")
         users = cur2.fetchall()
         cur.close()
         cur2.close()
         conn.close()
         
         for user in users:
            if (user[2] == row[4]):
               return_str += "<option value='" + str(user[0]) + ' ' + str(user[1]) + "' selected='selected'>" + str(user[0]) + ' ' + str(user[1]) + "</option>"
            else:
               return_str += "<option value='" + str(user[0]) + ' ' + str(user[1]) + "'>" + str(user[0]) + ' ' + str(user[1]) + "</option>"
         
         return_str += (    "</select>"
                            "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "<button type=\"button\" style=\"background-color:FireBrick\" onclick=\"location.href='delete_location?lid=" + lid + "';\">Delete</button>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                       )
                      
         return return_str
         
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
   
   else:
      return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page executes the update query on the database.
#----------------------------------------------------------------------------
@app.route('/edit_location_action', methods=['GET', 'POST'])
def edit_location_action():
   lid = request.args.get('lid')
   loc_name = request.form['loc_name']
   loc_address = request.form['loc_address']
   loc_descr = request.form['loc_descr']
   loc_super = request.form['loc_super']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT fname, lname, uid FROM user")
         users = cur.fetchall()
         
         sup_uid = 0
         for user in users:
            full_name = str(user[0]) + ' ' + str(user[1])
            if (full_name == loc_super):
               sup_uid = user[2]
         
         cur2 = conn.cursor()
         cur2.execute("UPDATE Locations SET Loc_Name = ?, Address = ?, Description = ?, Sup_uid = ? WHERE lid = ?", (loc_name, loc_address, loc_descr, sup_uid, int(lid)))
         conn.commit()
         cur.close()
         cur2.close()
         conn.close()
         
         #Redirect back to the locations page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/locations"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page allows the user to insert a new location on the database.
#----------------------------------------------------------------------------
@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
   database = "../SCADADB.db"
   conn = create_connection(database)
   return_str = pages.add_location_page
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT fname, lname FROM user")
         rows = cur.fetchall()
         for row in rows:
            return_str += "<option value='" + str(row[0]) + ' ' + str(row[1]) + "'>" + str(row[0]) + ' ' + str(row[1]) + "</option>"
            
         return_str += (   "</select>"
                           "<div style='text-align:center'>"
                            "<input type='submit' value='Save'>"
                            "</div>"
                          "</form>"
                        "</div>"
                        "</body>"
                        "</html>"
                       )
                       
      except Error as e:
         return_str += str(e)
   
   else:
      return_str += 'error retrieving points'
   
   return return_str

#----------------------------------------------------------------------------
#This page executes the insertion on the database.
#----------------------------------------------------------------------------
@app.route('/add_location_action', methods=['GET', 'POST'])
def add_location_action():
   loc_name = request.form['loc_name']
   loc_address = request.form['loc_address']
   loc_descr = request.form['loc_descr']
   loc_super = request.form['loc_super']
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("SELECT fname, lname, uid FROM user")
         users = cur.fetchall()
         
         sup_uid = 0
         for user in users:
            full_name = str(user[0]) + ' ' + str(user[1])
            if (full_name == loc_super):
               sup_uid = user[2]
         
         cur2 = conn.cursor()
         cur2.execute("INSERT INTO Locations (Loc_Name, Address, Description, Sup_uid) VALUES (?, ?, ?, ?)", (loc_name, loc_address, loc_descr, sup_uid))
         conn.commit()
         cur.close()
         cur2.close()
         conn.close()
         
         #Redirect back to the users page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/locations"></head></html>'
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#This page deletes a user from the database.
#----------------------------------------------------------------------------
@app.route('/delete_location', methods=['GET', 'POST'])
def delete_location():
   lid = request.args.get('lid')
   
   database = "../SCADADB.db"
   conn = create_connection(database)
   
   if (conn != None):
      try:
         cur = conn.cursor()
         cur.execute("DELETE FROM Locations WHERE lid = ?", (int(lid),))
         conn.commit()
         cur.close()
         conn.close()
         
         #Redirect back to the users page
         return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/locations"></head></html>'
         return 
      
      except Error as e:
         return '<!DOCTYPE html><html><h1>' + str(e) + '</h1></html>'
         
   return '<!DOCTYPE html><html><h1>Error connecting to the database!</h1></html>'

#----------------------------------------------------------------------------
#Creates a connection with the SQLite database.
#----------------------------------------------------------------------------
""" Create a connection to the database file """
def create_connection(db_file):
   try:
      conn = sqlite3.connect(db_file)
      return conn
   except Error as e:
      print(e)

   return None

#----------------------------------------------------------------------------
#Main dummy function. Only displays a message and exits. The app keeps
#running on the background by Flask
#----------------------------------------------------------------------------
def main():
   print("Starting the web interface...")
   
if __name__ == '__main__':
   main()