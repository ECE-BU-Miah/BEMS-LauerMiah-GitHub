import socket
from urllib.request import urlopen
from xml.dom import minidom
import requests
import time

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
            # print(data)
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
    of the device. For the WeMo, the following parameters will be obtained.
    '''
    metadata = dict()
    setupUrl = url + '/setup.xml'
    response = requests.get(setupUrl)
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
    return metadata


def getState(url):
    '''
    Uses XML SOAP requests to get the device state.
    '''
    header = {
        'Content-Type': 'text/xml; charset=utf=8',
        'SOAPACTION': '"urn:Belkin:service:basicevent:1#GetBinaryState"'
    }
    body = "<?xml version='1.0' encoding='utf-8'?>"\
           "<s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/' s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding'>"\
           "<s:Body>"\
           "<u:GetBinaryState xmlns:u='urn:Belkin:service:basicevent:1'>"\
           "</u:GetBinaryState>"\
           "</s:Body>"\
           "</s:Envelope>"
    if url is not None:
        baseUrl = url
    else:
        baseUrl = url
    print(baseUrl)
    response = requests.post(baseUrl + '/upnp/control/basicevent1', body, headers = header)
    dom = minidom.parseString(response.content)
    print(dom.getElementsByTagName('BinaryState')[0].firstChild.data)
    binaryState = dom.getElementsByTagName('BinaryState')[0].firstChild.data
    if(int(binaryState) > 0):
        return 'ON'
    elif(int(binaryState) == 0):
        return 'OFF'

def setState(state, url):
    '''
    Uses XML SOAP requests to set the device state (ON or OFF).
    '''
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
    if url is not None:
        baseUrl = url
    else:
        baseUrl = url

    response = requests.post(baseUrl + '/upnp/control/basicevent1', body, headers=header)
    dom = minidom.parseString(response.content)
    status = dom.getElementsByTagName('BinaryState')[0].firstChild.data
    print(status)

if __name__ == '__main__':
    # urls = wemo.findDevices()
    state = getState(url='http://192.168.0.30:49153')
    # print(urls)
    print('state: ' + str(state))
    setState(1, url='http://192.168.0.30:49153')
    state = getState(url='http://192.168.0.30:49153')
    print('state: ' + str(state))
    time.sleep(1)
    setState(0, url='http://192.168.0.30:49153')
    print(findMetadata(url='http://192.168.0.30:49153'))
