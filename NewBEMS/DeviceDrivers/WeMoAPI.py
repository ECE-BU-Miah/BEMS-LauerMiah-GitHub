import socket
from urllib.request import urlopen
from xml.dom import minidom
import requests
import time
from urllib.parse import urlparse
import global_settings
import sqlite3

BUFFERSIZE = 65507
TIMEOUT = 3

def findDevices():
    '''
    Use SSDP (Simple Service Discovery Protocol) to search
    for available WeMo devices on the network.
    '''
    urlList = list()
    multicast_group_ip = "239.255.255.250"
    multicast_group_port = 1900
    group = (multicast_group_ip, multicast_group_port)
    message = 'M-SEARCH * HTTP/1.1\r\n' \
              'HOST: {0}:{1}\r\n' \
              'MAN: "ssdp:discover"\r\n' \
              'ST: upnp:rootdevice\r\n' \
              'MX: 3\r\n' \
              '\r\n'.format(multicast_group_ip,
              multicast_group_port)

    s_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s_obj.settimeout(TIMEOUT)
    s_obj.sendto(message.encode('utf-8'), group)

    urlList = list()

    while True:
        try:
            data, addr = s_obj.recvfrom(BUFFERSIZE)
            data = data.decode('utf-8')
            data_list = data.split('\r\n')
            response_msg = data_list[0]
            headers = data_list[1:]
            for header in headers:
                if '49153/setup.xml' in header:
                    url = header.split(' ')[1]
                    pathBegin = url.rfind('/')
                    url = url[:pathBegin]
                    urlList.append(url)
                    # urlList.append(header.split(' ')[1])
        except socket.timeout:
            break # Allow to socket to read all responses until timeout occurs
    return urlList

def findMetadata(url):
    '''
    Accepts a URL and outputs a dictionary containing various properties
    of the device.
    '''
    metadata = dict()
    setupUrl = url + '/setup.xml'
    response = requests.get(setupUrl)
    parsedUrl = urlparse(url)
    netLocation = parsedUrl.netloc
    netLocationList = netLocation.split(':')
    ip = netLocationList[0]
    port = netLocationList[1]
    dom = minidom.parseString(response.content)
    try:
        macAddress = dom.getElementsByTagName('macAddress')[0].firstChild.data
        manufacturer = dom.getElementsByTagName('manufacturer')[0].firstChild.data
        friendlyName = dom.getElementsByTagName('friendlyName')[0].firstChild.data
    except Exception as e:
        pass
    metadata['macaddress'] = macAddress
    metadata['manufacturer'] = manufacturer
    metadata['name'] = friendlyName
    metadata['image'] = "wemoSwitchIcon.svg"
    metadata['api'] = "WeMo"
    metadata['ip'] = ip
    metadata['port'] = port

    # Data values that can obtained from the device
    metadata['queryable'] = 'power|onOffStatus'
    return metadata


def getState(deviceId, params, url=None):
    '''
    Uses XML SOAP requests to get the device state. Two different devices
    parameters will be queryable from the Switch: power and binary state.
    Params is a list.
    '''
    conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
    curs = conn.cursor()
    retDict = {}

    body = "<?xml version='1.0' encoding='utf-8'?>" \
            "<s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/' s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'>" \
            "<s:Body>" \
            "<u:GetInsightParams xmlns:u='urn:Belkin:service:insight:1'>" \
            "</u:GetInsightParams>" \
            "</s:Body>" \
            "</s:Envelope>"

    header = {
        'Content-Type': 'text/xml; charset="utf-8"',
        'SOAPACTION': '"urn:Belkin:service:insight:1#GetInsightParams"'
    }

    if url is None:
        curs.execute("SELECT ip, port FROM ActiveDevices WHERE id = ?;", (deviceId))
        networkCreds = curs.fetchall()
        deviceIp = networkCreds[0][0]
        devicePort = networkCreds[0][1]
        baseUrl = 'http://' + deviceIp + ':' + devicePort
    else:
        baseUrl = url
    response = requests.post(baseUrl + '/upnp/control/insight1', body, headers = header)

    dom = minidom.parseString(response.content)
    state = dom.getElementsByTagName('InsightParams')[0].firstChild.data

    "State|Seconds of last state change|last on seconds|Seconds on today|unknown|Total Seconds|unknown|Power(mW)|" \
                      "Energy used today (mW*min)|Energy used total (mW*min)|unknown"

    stateList = state.split('|')
    print(stateList)
    for param in params:
        if param == "power":
            retDict["power"] = float(stateList[7]) / 1000.0;
        elif param == "binaryState":
            retDict["binaryState"] = "ON" if int(stateList[0]) else "OFF"
    return retDict

def setState(deviceId, state):
    '''
    Uses XML SOAP requests to set the device state (ON or OFF).
    '''
    conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
    curs = conn.cursor()

    header = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPACTION': '"urn:Belkin:service:basicevent:1#SetBinaryState"'
    }
    body = "<?xml version='1.0' encoding='utf-8'?>"\
           "<s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'" \
           "s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'>" \
           "<s:Body>"\
           "<u:SetBinaryState xmlns:u='urn:Belkin:service:basicevent:1'>"\
           "<BinaryState>"+ str(state) + "</BinaryState>"\
           "</u:SetBinaryState>"\
           "</s:Body>"\
           "</s:Envelope>"
    curs.execute("SELECT ip, port FROM ActiveDevices WHERE id = ?;", (deviceId))
    networkCreds = curs.fetchall()
    deviceIp = networkCreds[0][0]
    devicePort = networkCreds[0][1]
    baseUrl = 'http://' + deviceIp + ':' + devicePort
    response = requests.post(baseUrl + '/upnp/control/basicevent1', body, headers=header)
    dom = minidom.parseString(response.content)
    status = dom.getElementsByTagName('BinaryState')[0].firstChild.data
    print(status)

if __name__ == '__main__':
    # # urls = wemo.findDevices()
    # state = getState(url='http://192.168.0.20:49153')
    # # print(urls)
    # print('state: ' + str(state))
    # setState(1, url='http://192.168.0.20:49153')
    # state = getState(url='http://192.168.0.20:49153')
    # print('state: ' + str(state))
    # time.sleep(1)
    # setState(0, url='http://192.168.0.20:49153')
    # print(findMetadata(url='http://192.168.0.20:49153'))
    print("Finding devices")
    print(findDevices())
    state = getState(None,['power', 'binaryState'],'http://192.168.0.18:49153')
    print(state)
