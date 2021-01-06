import bottle
import csv
import json
import os.path
import urllib.request
import urllib.parse
import sqlite3

def filterIn(lst, k, v):
    acc = []
    for d in lst:
        if k in d and d[k] == v:
            acc.append(d)
    return acc

def filterOut(lst, k, v):
    acc = []
    for d in lst:
        if k in d and d[k] != v:
            acc.append(d)
    return acc

def filterInRange(lst, k, low, high):
    acc = []
    for d in lst:
        if k in d and float(d[k]) >= low and float(d[k]) < high:
            acc.append(d)
    return acc

def filterByMonth(lst, m):
    acc = []
    k = 'EndDt_DtFin'
    for d in lst:
        if k in d:
            date = d[k]
            month = int(date[5:7])
            if month == m:
                acc.append(d)
    return acc

def filterByYear(lst, y):
    acc = []
    k = "EndDt_DtFin"
    for d in lst:
        if k in d:
            date = d[k]
            year = int(date[0:4])
            if year == y:
                acc.append(d)
    return acc

def makeDictionary(headers, data):
    dict = {}
    for i in range(len(headers)):
        dict[headers[i]] = data[i]
    return dict

def readDataFromCSVFile(filename):
    data = []
    with open(filename, newline='') as file:
        csvReader = csv.reader(file)
        headerRow = True
        for record in csvReader:
            if headerRow:
                headers = record
                headerRow = False
            else:
                data.append(makeDictionary(headers, record))
    return data

def dictionaryToListOfValues(keys, d):
    listOfValues = []
    for k in keys:
        listOfValues.append(d[k])
    return listOfValues

def writeDataToCSVFile(filename, data, keys, headerRow):
    with open(filename, 'w') as file:
        csvWriter = csv.writer(file)
        if headerRow:
            csvWriter.writerow(keys)
        for dict in data:
            csvWriter.writerow(dictionaryToListOfValues(keys, dict))

def loadData(filenameRoot):
   csvFile = filenameRoot
   if not os.path.isfile(csvFile):
       uri = "https://od-do.agr.gc.ca/WeeklyPoultrySlaughter_AbattageVolailleHebdomadaire.json"
       response = urllib.request.urlopen(uri)
       content_string = response.read().decode()
       content = json.loads(content_string)
       writeDataToCSVFile(csvFile,content["WeeklyPoultrySlaughter_AbattageVolailleHebdomadaire"],["EndDt_DtFin","MjrCmdtyEn_PrdtPrncplAn","CtgryEn_CtgrieAn","NumHd_NmbTetes"],True)

def pieData(read):
  data = {"values":[], "labels":[],"type":"pie"}
  for s in read:
    if s["MjrCmdtyEn_PrdtPrncplAn"] in data["labels"]:
      data["values"][data["labels"].index(s["MjrCmdtyEn_PrdtPrncplAn"])] += int(s["NumHd_NmbTetes"])
    else:
      data["values"].append(int(s["NumHd_NmbTetes"]))
      data["labels"].append(s["MjrCmdtyEn_PrdtPrncplAn"])
  addPieData(data["labels"],data["values"])
  layout = {"title":"Poultry Slaughter In Canada" ,"height": 400, "width": 600}
  retVal = {"layout":layout, "data":[data], "div":"pie"}
  return json.dumps(retVal)

def pieByYear(read, year):
  data = {"values":[], "labels":[],"type":"pie"}
  for s in read:
    if s["MjrCmdtyEn_PrdtPrncplAn"] in data["labels"]:
      data["values"][data["labels"].index(s["MjrCmdtyEn_PrdtPrncplAn"])] += int(s["NumHd_NmbTetes"])
    else:
      data["values"].append(int(s["NumHd_NmbTetes"]))
      data["labels"].append(s["MjrCmdtyEn_PrdtPrncplAn"])
  addPieData(data["labels"],data["values"])
  layout = {"title": "Poultry In Canada " + str(year) ,"height": 400, "width": 600}
  return {"layout":layout, "data":[data], "div":"pie"}

def bubbly(read):
  lst = []
  addBubbleData([],True)
  for s in range(1997,2020):
    tempData = {"x":["Turkey", "Chicken", "Ducks/Geese", "Mature Chicken"],"y":[0,0,0,0],"name":s,"mode":"markers","marker":{"color":['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],"size": [40, 60, 80, 100]}}
    temp = filterByYear(read,s)
    for d in temp:
      tempData["y"][tempData["x"].index(d["MjrCmdtyEn_PrdtPrncplAn"])] += int(d["NumHd_NmbTetes"])
  
    lst.append(tempData)
  addBubbleData(lst,False)
  layout = {"title": "Poultry In Canada","height": 800, "width": 800, "yaxis":{"dtick":1000000,"tick0":0},"showLegend":False}
  return json.dumps({"layout":layout, "data":lst, "div":"bub"})

def bubByMonth(read):
  tempLst = ["January", "February", "March", "April","May","June","July","August","September","October","November","December"]
  addBubbleData([],True)
  for s in range(0,12):
    temp = filterByMonth(read,s+1)
    for d in temp:
      tempData["y"][s] += int(d["NumHd_NmbTetes"])
  addBubbleData([tempData],False)
  layout = {"title": "Poultry Slaughter In Canada","height": 800, "width": 800, "yaxis":{"dtick":1000000,"tick0":0},"showLegend":False}
  return json.dumps({"layout":layout, "data":[tempData], "div":"bub"})

def bubChange(read):
  lst = []
  addBubbleData(lst,True)
  for s in range(1997,2020):
    tempData = {"y":["Turkey", "Chicken", "Ducks/Geese", "Mature Chicken"],"x":[0,0,0,0],"name":s,"mode":"markers","marker":{"color":['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],"size": [40, 60, 80, 100]}}
    temp = filterByYear(read,s)
    for d in temp:
      tempData["x"][tempData["y"].index(d["MjrCmdtyEn_PrdtPrncplAn"])] += int(d["NumHd_NmbTetes"])
  
    lst.append(tempData)
  addBubbleData(lst,False)
  layout = {"title": "Poultry Slaughter In Canada","height": 800, "width": 800, "xaxis":{"dtick":1000000,"tick0":0},"showLegend":False}
  return json.dumps({"layout":layout, "data":lst, "div":"bub"})

def addPieData(data1,data2):
  conn = sqlite3.connect("data.db")
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS pie")
  cur.execute("CREATE TABLE IF NOT EXISTS pie (Type,Amount)")
  for s in range(0, len(data1)):
    cur.execute("INSERT INTO pie VALUES (?,?)", (data1[s],data2[s]))
  conn.commit()
  conn.close()

def addBubbleData(data,drop):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    if drop:
      cur.execute("DROP TABLE IF EXISTS bubble")
      cur.execute("CREATE TABLE IF NOT EXISTS bubble (Name,Type,Amount)")
    else:
      for s in data:
        for d in range(0, len(s["x"])):
          cur.execute("INSERT INTO bubble VALUES (?,?,?)",(s["name"],s["x"][d],s["y"][d]))
          
    conn.commit()
    conn.close()

def readData():
  conn = sqlite3.connect("data.db")
  cur = conn.cursor()
  string = ""
  for s in cur.execute("SELECT * FROM bubble"):
    string += s

  return json.dumps(string)