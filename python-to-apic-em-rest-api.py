import requests
import json

requests.packages.urllib3.disable_warnings()  # Disable warnings

# Controller settings
CONTROLLER_IP = "10.10.20.60"
USER = "admin"
PASS = "Cisco12345"
GET = "get"
POST = "post"


def getServiceTicket():
    ticket = None
    payload = {"username": USER, "password": PASS}

    # This is the URL to get the service ticket.
    url = "https://" + CONTROLLER_IP + "/api/v1/ticket"

    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Format the payload to JSON and add to the data.  Include the header in the call.
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)

    # Data received.  Get the ticket and print to screen.
    r_json = response.json()
    ticket = r_json["response"]["serviceTicket"]
    return ticket


# Make the REST call using the service ticket, command, http url, data for the body (if any)
def doRestCall(aTicket, command, url, aData=None):
    response_json = None
    payload = None

    # if data for the body is passed in put into JSON format for the payload
    if (aData != None):
        payload = json.dumps(aData)

    # add the service ticket and content type to the header
    header = {"X-Auth-Token": aTicket, "content-type": "application/json"}
    if (command == GET):
        r = requests.get(url, data=payload, headers=header, verify=False)
    elif (command == POST):
        r = requests.post(url, data=payload, headers=header, verify=False)
    else:
        # if the command is not GET or POST we dont handle it.
        print ("Unknown command!")
        return

    # if no data is returned print a message; otherwise print data to the screen
    if (not r):
        print("No data returned!")
    else:

        # put into dictionary format
        response_json = r.json()
        device_list = response_json['response']
        # print device_list            #print out the response in 'JSON' format

        try:
            for device in device_list:
                print 'Name of device: %s' % device['hostname']
                print 'IP of device: %s' % device['managementIpAddress']
                print 'MAC address of device: %s' % device['macAddress']
                print 'Device type: %s' % device['type']
                print 'Device Series: %s' % device['series']
                print 'Device Platform Id: %s' % device['platformId']
                print 'Device Family: %s' % device['family']
                print 'Device Role: %s' % device['role']
                print '---'
        except:
            pass


# Call the function to get the service ticket
ticket = getServiceTicket()

# Get network device info in the system
doRestCall(ticket, GET, "https://" + CONTROLLER_IP + "/api/v1/network-device")

# Create a new application
# doRestCall(ticket, POST, "https://" + CONTROLLER_IP + "/api/v1/topology/application",[{"id":"1","description":"cool app","name":"appABC"}])
