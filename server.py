import json
import bottle
import App

#The "/" route serves up a single HTML page as a static file. 
@bottle.route("/")
def serve_html():
  return bottle.static_file("index.html", root=".")

#A  route to serve up the front end JavaScript code as a static file.  
@bottle.route("/script.js")
def serve_front_end_js():
  return bottle.static_file("script.js", root=".")

#A route to serve up the AJAX JavaScript code as a static file.  
@bottle.route("/ajax.js")
def serve_AJAX():
  return bottle.static_file("ajax.js", root=".")




# recover the JSON blob that carries the data,
# convert the JSON blog to Python data,
# call the App.data_by_months function with that data as argument, and
# return the data that function provides, encoded as a JSON string.
@bottle.post("/table")
def serve_table():
  content = bottle.request.body.read().decode()
  content = json.loads(content) #content is the dictionary as: {"loan_amount": loanAmount, "annual_interest_rate": annualInterestRate, "loan_term_length": loanTermLength} in json format
  data = App.data_by_months(content)
  return json.dumps(data)




