import bottle
import json
import appcode


@bottle.route("/")
def handleRequestHTML():
    return bottle.static_file("index.html", root="")

@bottle.route("/java.js")
def handleRequestCode():
    return bottle.static_file("java.js", root="")

@bottle.route("/pieChart")
def foo():
  return appcode.pieData(appcode.readDataFromCSVFile('data.csv'))

@bottle.route("/bubbleChart")
def foo():
  return appcode.bubbly(appcode.readDataFromCSVFile('data.csv'))

@bottle.route("/bubbleMonth")
def foo():
  return appcode.bubByMonth(appcode.readDataFromCSVFile('data.csv'))

@bottle.route("/bubbleChange")
def foo():
  return appcode.bubChange(appcode.readDataFromCSVFile('data.csv'))

@bottle.route("/test")
def foo():
  return appcode.readData()

@bottle.post("/sendPie")
def foo():
  content = bottle.request.body.read()
  content = content.decode()
  content_ = json.loads(content)
  rawData = appcode.readDataFromCSVFile("data.csv")
  data = appcode.filterByYear(rawData,int(content))
  return json.dumps(appcode.pieByYear(data, int(content)))

appcode.loadData("data.csv")

bottle.run(host = '0.0.0.0', port='8080', debug=True)
