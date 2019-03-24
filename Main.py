# Input the city name part
# Read a city's name from the GUI
import sys
from PyQt5.QtWidgets import *

# Solve the kernel restarting problem
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
# Generate a QInputDialog
dlg = QInputDialog()
# Set mode
dlg.resize(250,150)
dlg.setInputMode(0)
dlg.setTextEchoMode(QLineEdit.Normal)
dlg.setLabelText("请输入城市名称:")
dlg.setWindowTitle("城市空气质量查询")
# Set the button
dlg.setOkButtonText(u"确认")
dlg.setCancelButtonText(u"取消")
if dlg.exec_():
    cityname = dlg.textValue()
dlg.show()


# Get part
import requests
import json

# Get the CO value of this city
url = 'http://www.pm25.in/api/querys/co.json?city=%s&token=5j1znBVAsnSf5xQyNQyq'%(cityname)
r = requests.get(url)
# Use json to parse
hjson = json.loads(r.text)


# Analysis part
from Class import Position

# Put the hjson list's data into Class Position
place_list = [Position(place['position_name'],place['aqi'],place['co'],place['co_24h']) for place in hjson]
# Establish several lists to save different living-friendly levels' positions
livable_place = [livap for livap in place_list if livap.judge_livable() == "livable"]
unhealthy_place = [unhealp for unhealp in place_list if unhealp.judge_livable() == "unhealthy"]
dangerous_place = [dangerp for dangerp in place_list if dangerp.judge_livable() == "dangerous"]
# Establish several lists to save different positions' protections
noprotect_place = [npp for npp in place_list if npp.protection() == "none"]
mask_place = [mkp for mkp in place_list if mkp.protection() == "mask"]
indoor_place = [idp for idp in place_list if idp.protection() == "indoor"]
# Establish several lists to save different positions' stay-suggestions
stay_place = [stp for stp in place_list if stp.judge_stay() == "stay"]
consider_place = [csdp for csdp in place_list if csdp.judge_stay() == "consider"]
leave_place = [lvp for lvp in place_list if lvp.judge_stay() == "leave"]


# Output part
# In this part the output information will be showed on the GUI
# Output livable, unhealthy and dangerous places in this city
# State the judge standard
QMessageBox.about(dlg,"宜居性标准","AQI指数不超过75判定为'宜居'\nAQI指数介于75至300判定为'轻度不健康'\nAQI大于300判定为'危险'")
# Define a function to sort empty list
def outputlive_sort(dict):
    for key in dict:
        if len(dict[key]) == 0:
            # Set a massagebox to show the information
            QMessageBox.about(dlg,"宜居性","%s市没有地方是%s的"%(cityname,key))
        else:
            QMessageBox.about(dlg,"宜居性","在%s市的这些地点附近是%s的："%(cityname,key))
            outputlive(dict[key])

# Define a function to output places
def outputlive(list):
    # Set a string to save the place name list
    postr = ''
    for tmp in list:
        if tmp.position_name != None:
            postr = postr + tmp.position_name + ' '
    QMessageBox.about(dlg,"宜居性",postr)

outputlive_sort({'宜居':livable_place,'轻度不健康':unhealthy_place,'危险':dangerous_place})

# Output a place's suggested protection
QMessageBox.about(dlg,"防护措施标准","不同建议的判定依据为CO实时浓度\n分界值分别为1.0mg/m3和3.0mg/m3")
def outputprot_sort(dict):
    for key in dict:
        if len(dict[key]) != 0:
            QMessageBox.about(dlg,"防护措施","在%s市的这些地点附近我们建议您%s："%(cityname,key))
            outputprot(dict[key])

def outputprot(list):
    postr = ''
    for tmp in list:
        if tmp.position_name != None:
            postr = postr + tmp.position_name + ' '
    QMessageBox.about(dlg,"防护措施",postr)
            
outputprot_sort({'什么也不做':noprotect_place,'戴上吸收CO的口罩':mask_place,'停留在室内':indoor_place})

# Output the suggestion of whether a place should be stayed long in or not
QMessageBox.about(dlg,"久留建议标准","不同建议的判定依据为CO的24小时平均浓度\n分界值分别为0.5mg/m3和1.0mg/m3")
def outputstay_sort(dict):
    for key in dict:
        if len(dict[key]) != 0:
            QMessageBox.about(dlg,"久留建议","在%s市的这些地点附近您%s："%(cityname,key))
            outputstay(dict[key])

def outputstay(list):
    postr = ''
    for tmp in list:
        if tmp.position_name != None:
            postr = postr + tmp.position_name + ' '
    QMessageBox.about(dlg,"久留建议",postr)
            
outputstay_sort({'可以久留':stay_place,'应该三思':consider_place,'应该离开':leave_place})

# Stop the GUI
sys.exit(app.exec_())