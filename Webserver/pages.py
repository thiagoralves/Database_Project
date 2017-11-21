login_page = ( "<!DOCTYPE html>"
               "<html>"
               "<style>"
               "form {"
                   "border: 3px solid #f1f1f1;"
               "}"
               "input[type=text], input[type=password] {"
                   "width: 100%;"
                   "font-family: arial, sans-serif;"
                   "padding: 12px 20px;"
                   "margin: 8px 0;"
                   "display: inline-block;"
                   "border: 1px solid #ccc;"
                   "box-sizing: border-box;"
               "}"
               "h1 {"
                  "font-family: arial, sans-serif;"
                  "border-collapse: collapse;"
                  "width: 100%;"
               "}"
               "button {"
                   "background-color: #4CAF50;"
                   "color: white;"
                   "font-family: arial, sans-serif;"
                   "padding: 14px 20px;"
                   "margin: 8px 0;"
                   "border: none;"
                   "cursor: pointer;"
                   "width: 100%;"
               "}"
               "button:hover {"
                   "opacity: 0.8;"
               "}"
               "</style>"
               "<body>"
               "<h1><center>Real-Time PLC Monitor Login</center></h1>"
               "<form action='/check_login' method='post'>"
                 "<div class='container'>"
                   "<label><b>Username</b></label>"
                   "<input type='text' placeholder='Enter Username' name='uname' required>"
                   "<label><b>Password</b></label>"
                   "<input type='password' placeholder='Enter Password' name='psw' required> "
                   "<button type='submit'>Login</button>"
                 "</div>"
               "</form>"
               "</body>"
               "</html>"
            )

default_pages_header = (   " <!DOCTYPE html>"
                           "<html>"
                           "<head>"
                           "<meta name='viewport' content='width=device-width, user-scalable=no'>"
                           "<style>"
                           ".top {"
                               "position:absolute;"
                               "left:0; right:0;"
                               "height: 92px;"
                               "background-color: dimgray;"
                           "}"
                           ".left {"
                               "position:absolute;"
                               "left:0; top:100px; bottom: 0;"
                               "width: 178px;"
                               "background-color: #dddddd;"
                           "}"
                           ".main {"
                               "position: absolute;"
                               "left:200px; top:100px; right:0; bottom:0;"
                           "}"
                           "label {"
                               "font-family: arial, sans-serif;"
                           "}"
                           "input[type=text], select {"
                               "width: 100%;"
                               "padding: 12px 20px;"
                               "margin: 8px 0;"
                               "display: inline-block;"
                               "border: 1px solid #ccc;"
                               "border-radius: 4px;"
                               "box-sizing: border-box;"
                               "font-family: arial, sans-serif;"
                           "}"
                           "button, input[type=submit] {"
                               "background-color: #4CAF50;"
                               "color: white;"
                               "font-family: arial, sans-serif;"
                               "padding: 14px 20px;"
                               "margin: 8px 0;"
                               "border: none;"
                               "cursor: pointer;"
                               "width: 300px;"
                           "}"
                           "button, input[type=submit]:hover {"
                               "opacity: 0.8;"
                           "}"
                           "table, h1, h2, h3, p {"
                               "font-family: arial, sans-serif;"
                               "border-collapse: collapse;"
                               "width: 100%;"
                           "}"
                           "td, th {"
                               "border: 1px solid #dddddd;"
                               "text-align: left;"
                               "padding: 8px;"
                           "}"
                           "tr:nth-child(even) {"
                               "background-color: #dddddd;"
                           "}"
                           "tr:hover {"
                             "cursor: hand;"
                             "background-color: slategray;"
                           "}"
                           "a {"
                              "color:black;"
                               "font-family: arial, sans-serif;"
                               "text-decoration: none;"
                           "}"
                           "</style>"
                           "<script type='text/javascript'>"
                           "function filterPointsTable(a) {"
                             "document.location='/points?filter_by=' + a.value"
                           "}"
                           "</script>"
                           "</head>"
                           "<body>"
                           "<div class='top'>"
                               "<h1 style='color:white'><center>Real-Time PLC Monitor</center></h1>"
                           "</div>"
                           "<div class='left'>"
                               "<p><b><h3 style='text-decoration:underline'>Menu</h3><br><a href='/locations'>Manage Locations</a><br><br><a href='/devices'>Manage Devices</a><br><br><a href='/points'>Manage Points</a><br><br><a href='/view'>View Point Data</a><br><br><a href='users'>Manage Users</a><br><br><a href='/'>Logout</a></b></p>"
                           "</div>"
                           "<div class='main'>"
                        )
                        
device_page_header = default_pages_header + ("<h2>PLC Devices<br></h2>"
                                                "<table>"
                                                  "<tr style='background-color: white'>"
                                                   "<th>Device Name</th><th>IP</th><th>Port</th><th>Location</th>"
                                                  "</tr>"
                                            )

point_page_header = default_pages_header + ("<h2>PLC Points<br></h2>"
                                                "<h3>Filter by Device:"
                                                "<select onChange=\"filterPointsTable(this)\" style='width:400px'>"
                                                "<option value='All'>All</option>"
                                           )
                                            
add_device_page = default_pages_header + ("<h2>Insert Device</h2>"
                                               "<form action='/add_device_action' method='post'>"
                                                    "<label for='devname'>Device Name</label>"
                                                    "<input type='text' id='devname' name='dev_name' placeholder='Temperature Control PLC'>"
                                                    "<label for='ip'>IP</label>"
                                                    "<input type='text' id='ip' name='dev_ip' placeholder='100.100.100.251'>"
                                                    "<label for='port'>Port</label>"
                                                    "<input type='text' id='port' name='dev_port' placeholder='502'>"
                                                    "<label for='locName'>Location</label>"
                                                    "<select id='locName' name='loc_name'>"
                                         )

add_point_page = default_pages_header + ("<h2>Insert Point</h2>"
                                               "<form action='/add_point_action' method='post'>"
                                                    "<label for='pointName'>Point Name</label>"
                                                    "<input type='text' id='pointName' name='point_name' placeholder='Temperature Sensor'>"
                                                    "<label for='pointAddress'>Address</label>"
                                                    "<input type='text' id='pointAddress' name='point_address' placeholder='0'>"
                                                    "<label for='pointType'>Type</label>"
                                                    "<select id='pointType' name='point_type'>"
                                                    "<option value='dig_in'>dig_in</option>"
                                                    "<option value='dig_out'>dig_out</option>"
                                                    "<option value='an_in'>an_in</option>"
                                                    "<option value='an_out'>an_out</option>"
                                                    "</select>"
                                                    "<label for='multFact'>Multiplication Factor</label>"
                                                    "<input type='text' id='multFact' name='mult_fact' placeholder='1.0'>"  
                                                    "<label for='pointDescription'>Description</label>"
                                                    "<input type='text' id='pointDescription' name='point_description' placeholder='Description...'>"                                                    
                                                    "<label for='devName'>Device</label>"
                                                    "<select id='devName' name='dev_name'>"
                                        )

view_point_header = (      "<style>"
                           ".top {"
                               "position:absolute;"
                               "left:0; right:0;"
                               "height: 92px;"
                               "background-color: dimgray;"
                           "}"
                           ".left {"
                               "position:absolute;"
                               "left:0; top:100px; bottom: 0;"
                               "width: 178px;"
                               "background-color: #dddddd;"
                           "}"
                           ".main {"
                               "position: absolute;"
                               "left:200px; top:100px; right:0; bottom:0;"
                           "}"
                           "label {"
                               "font-family: arial, sans-serif;"
                           "}"
                           "input[type=text], select {"
                               "width: 100%;"
                               "padding: 12px 20px;"
                               "margin: 8px 0;"
                               "display: inline-block;"
                               "border: 1px solid #ccc;"
                               "border-radius: 4px;"
                               "box-sizing: border-box;"
                               "font-family: arial, sans-serif;"
                           "}"
                           "button, input[type=submit] {"
                               "background-color: #4CAF50;"
                               "color: white;"
                               "font-family: arial, sans-serif;"
                               "padding: 14px 20px;"
                               "margin: 8px 0;"
                               "border: none;"
                               "cursor: pointer;"
                               "width: 300px;"
                           "}"
                           "button, input[type=submit]:hover {"
                               "opacity: 0.8;"
                           "}"
                           "table, h1, h2, h3, p {"
                               "font-family: arial, sans-serif;"
                               "border-collapse: collapse;"
                               "width: 100%;"
                           "}"
                           "td, th {"
                               "border: 1px solid #dddddd;"
                               "text-align: left;"
                               "padding: 8px;"
                           "}"
                           "tr:nth-child(even) {"
                               "background-color: #dddddd;"
                           "}"
                           "tr:hover {"
                             "cursor: hand;"
                             "background-color: slategray;"
                           "}"
                           "a {"
                              "color:black;"
                               "font-family: arial, sans-serif;"
                               "text-decoration: none;"
                           "}"
                           "</style>"
                           "<script type='text/javascript'>"
                           "function filterViewPoints(a) {"
                             "document.location='/view?filter_by=' + a.value"
                           "}"
                           "</script>"
                           "</head>"
                           "<body>"
                           "<div class='top'>"
                               "<h1 style='color:white'><center>Real-Time PLC Monitor</center></h1>"
                           "</div>"
                           "<div class='left'>"
                               "<p><b><h3 style='text-decoration:underline'>Menu</h3><br><a href='/locations'>Manage Locations</a><br><br><a href='/devices'>Manage Devices</a><br><br><a href='/points'>Manage Points</a><br><br><a href='/view'>View Point Data</a><br><br><a href='users'>Manage Users</a><br><br><a href='/'>Logout</a></b></p>"
                           "</div>"
                           "<div class='main'>"
                           "<h2>PLC Points<br></h2>"
                           "<h3>Filter by Device:"
                           "<select onChange=\"filterViewPoints(this)\" style='width:400px'>"
                           "<option value='All'>All</option>"
                  )

user_page_header = default_pages_header + ("<h2>Users<br></h2>"
                                                "<table>"
                                                  "<tr style='background-color: white'>"
                                                   "<th>First Name</th><th>Last Name</th><th>E-mail</th>"
                                                  "</tr>"
                                          )
                                          
add_user_page = default_pages_header + ("<h2>Add User</h2>"
                                               "<form action='/add_user_action' method='post'>"
                                                    "<label for='fname'>First Name</label>"
                                                    "<input type='text' id='fname' name='user_fname' placeholder='John'>"
                                                    "<label for='lname'>Last Name</label>"
                                                    "<input type='text' id='lname' name='user_lname' placeholder='Smith'>"
                                                    "<label for='email'>E-mail</label>"
                                                    "<input type='text' id='email' name='user_email' placeholder='john@smith.com'>"
                                                    "<label for='password'>Password</label>"
                                                    "<input type='text' id='password' name='user_pass' placeholder='12345'>" 
                                                    "<div style='text-align:center'>"
                                                    "<input type='submit' value='Save'>"
                                                    "</div>"
                                                  "</form>"
                                                "</div>"
                                                "</body>"
                                                "</html>"
                                       )
                                       
location_page_header = default_pages_header + ("<h2>Locations<br></h2>"
                                                "<table>"
                                                  "<tr style='background-color: white'>"
                                                   "<th>Location Name</th><th>Address</th><th>Description</th><th>Supervisor</th>"
                                                  "</tr>"
                                          )
                                          
add_location_page = default_pages_header + ("<h2>Add Location</h2>"
                                               "<form action='/add_location_action' method='post'>"
                                               "<label for='lname'>Location Name</label>"
                                               "<input type='text' id='lname' name='loc_name' placeholder='My Lab'>"
                                               "<label for='address'>Address</label>"
                                               "<input type='text' id='address' name='loc_address' placeholder='221b Baker St, London'>"
                                               "<label for='descr'>Description</label>"
                                               "<input type='text' id='descr' name='loc_descr' placeholder='Place to do stuff'>"
                                               "<label for='supervisor'>Supervisor</label>"
                                               "<select id='supervisor' name='loc_super'>"
                                           )