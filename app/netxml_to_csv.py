from lxml import etree
#from collections import OrderedDict

'''
Original script created by Meatballs1 to parse netxml-to-csv:
https://github.com/Meatballs1/NetXML-to-CSV
Source was modified to make it more compatible with JSON output.
'''

def associatedClients(network, bssid, essid_text):
    clients = network.getiterator('wireless-client')

    if clients is not None:
        client_info = list()

        for client in clients:
            mac = client.find('client-mac')
            if mac is not None:
                client_mac = mac.text
                snr = client.find('snr-info')
                if snr is not None:
                    power = client.find('snr-info').find('max_signal_dbm')
                    if power is not None:
                        dic = dict(clientmac=client_mac, clientpower=power.text)
                        client_info.append(dic)

        return client_info

def parse_net_xml(doc):

    total = len(list(doc.getiterator("wireless-network")))
    tenth = total/10
    count = 0
    clients = list()

    parsed_list = []

    for network in doc.getiterator("wireless-network"):
        count += 1
        try:
            if (count % tenth) == 0:
                continue
        except ZeroDivisionError:
            print("Division by zero error")

        type = network.attrib["type"]
        channel = network.find('channel').text
        bssid = network.find('BSSID').text

        if type == "probe" or channel == "0":
            continue

        encryption = network.getiterator('encryption')
        privacy = ""
        cipher = ""
        auth = ""
        if encryption is not None:
            for item in encryption:
                if item.text.startswith("WEP"):
                    privacy = "WEP"
                    cipher = "WEP"
                    auth = ""
                    break
                elif item.text.startswith("WPA"):
                    if item.text.endswith("PSK"):
                        auth = "PSK"
                    elif item.text.endswith("AES-CCM"):
                        cipher = "CCMP " + cipher
                    elif item.text.endswith("TKIP"):
                        cipher += "TKIP "
                elif item.text == "None":
                    privacy = "OPN"

        cipher = cipher.strip()

        if cipher.find("CCMP") > -1:
            privacy = "WPA2"

        if cipher.find("TKIP") > -1:
            privacy += "WPA"


        power = network.find('snr-info')
        dbm = ""
        if power is not None:
            dbm = power.find('max_signal_dbm').text

        if int(dbm) > 1:
            dbm = power.find('last_signal_dbm').text

        if int(dbm) > 1:
            dbm = power.find('min_signal_dbm').text

        ssid = network.find('SSID')
        essid_text = ""
        if ssid is not None:
            essid_text = network.find('SSID').find('essid').text

        gps = network.find('gps-info')
        lat, lon = '', ''
        if gps is not None:
            lat = network.find('gps-info').find('min-lat').text
            lon = network.find('gps-info').find('min-lon').text

        #
        data = dict(ESSID=essid_text, BSSID=bssid, Channel=channel, Privacy=privacy,
                    Cipher=cipher, Authenticaiton=auth, DBM=dbm)

        if lat and lon is not None:
            google_map = "https://maps.google.com/maps?q=" + lat + "," + lon + "&ll=" + lat + "," + lon + "&z=17"
            google_map_link = "<a href=\"" + google_map + "\" target=\"_blank\"> Google map link</a>"

            location = dict(Latitude=lat, Longitude=lon, Googlemap=google_map_link) # Add GPS info
        else:
            not_found = "Not coordinates available"
            location = dict(Latitude=not_found, Longitude=not_found)

        client_list = associatedClients(network, bssid, essid_text) # Return a dic list of client mac/power

        if client_list is not None:
                data['client'] = client_list #Add a client
        else:
            not_found = "No clients found"
            data['client'] = not_found

        data['location'] = location

        parsed_list.append(data) # add json to list

    return parsed_list

def process_net_xml(input):
    doc = etree.fromstring(input)
    parsed_list = parse_net_xml(doc) # Start the processing of file

    return parsed_list # Return processed json to kismet_log_viewer.py