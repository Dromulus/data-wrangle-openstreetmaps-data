import xml.etree.ElementTree as ET
import re
import codecs
import json

datafile = r'/home/kevin/Documents/projects/Udacity/Project_2/humboldt_bay_area'
fixname = {'St': 'Street'}


def street_clean(street):
    #Fix values which are not actually street names
    if street == 'Harrison':
        street = 'Harrison Avenue'
    if street == 'Nw Cnr Elk River Int':
        street = 'Pound Road'
    if street == 'Ne Cnr Trinidad Int':
        street = 'Trinidad Frontage Road'
    if street == 'Nw Cnr Trinidad Int':
        street = 'Patricks Point Drive'
    if street == 'Harris':
        street = 'Harris Street'
    if street == 'Alliance':
        street = 'Alliance Road'
    if street == 'Se Cnr Kenmar Road Int':
        street = 'Kenmar Road'
    if street == '1924 Smith Lane':
        street = 'Smith Lane'
    if street == 'Hwy 299 PM 12.4':
        street = 'Highway 299'
    if street == 'Broadway':
        street = 'Highway 101'
    if street == 'Myrtle':
        street = 'Myrtle Avenue'
    if street == '1835 6TH Street':
        street = '6th Street'
    if street == '6100 No Hwy 101':
        street = 'Highway 101'
    if street == '1656 Union Street':
        street == 'Union Street'
    if street == 'Broadway Street':
        street = 'Highway 101'
    #Fix abbreviations
    words = street.strip().split(' ')
    for word in words:
        if word in fixname.keys():
            street = street.replace(word, fixname[word])
    return street


def shape_element(element):
    node = {}
    #Check for and collect root level values
    if element.tag == "node" or element.tag == "way" :
        if 'id' in element.attrib.keys():
            node['id'] = element.attrib['id']
        node['type'] = element.tag
        if 'visible' in element.attrib.keys():
            node['visible'] = element.attrib['visible']
        if 'lat' in element.attrib.keys() and 'lon' in element.attrib.keys():
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        #create dictionary for nested 'created' values, try to fill dictionary
        created = {}
        if 'version' in element.attrib.keys():
            created['version'] = element.attrib['version']
        if 'changeset' in element.attrib.keys():
            created['changeset'] = element.attrib['changeset']
        if 'timestamp' in element.attrib.keys():
            created['timestamp'] = element.attrib['timestamp']
        if 'user' in element.attrib.keys():
            created['user'] = element.attrib['user']
        if 'uid' in element.attrib.keys():
            created['uid'] = element.attrib['uid']
        #Nest 'created' dictionary if values found
        if len(created) > 0:
            node['created'] = created

        #Create dictionaries for storing tag values to be nested
        address = {}
        name = {}
        gnis = {}
        tiger = {}
        alt_name = {}
        caltrans = {}
        nhd = {}
        county = {}
        fg = {}
        csp = {}
        ref = {}
        flag = {}
        old_name = {}
        fuel = {}
        toilets = {}
        monitoring = {}
        oneway = {}
        lanes = {}
        turn = {}
        park = {}
        contact = {}
        hgv = {}
        diet = {}
        boundary = {}
        payment = {}
        census = {}
        nist = {}
        internet_access = {}

        #Gather tag keys and values, incorporate instructions for nesting and corrections
        for item in element.iter('tag'):

            #skip tags with problem chars or multiple colons
            if re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]').search(item.attrib['k']) or re.compile(r'[:].+[:]').search(item.attrib['k']):
                continue

            #nest 'addr:' values in 'address' and remove 'addr:' from key
            elif item.attrib['k'][:5]== 'addr:':
                if item.attrib['k'] == 'addr:state':        #Capitalize state (e.g. 'Ca' to 'CA')
                    address[item.attrib['k'][5:]] = item.attrib['v'].upper()
                elif item.attrib['k'] == 'addr:street':     #Fix street abbreviations and correct values
                    address[item.attrib['k'][5:]] = street_clean(item.attrib['v'])
                elif item.attrib['k'] == 'addr:city':       #Format city names
                    if 'Arcata' in item.attrib['v']:
                        city = 'Arcata'
                    elif 'Fortuna' in item.attrib['v']:
                        city = 'Fortuna'
                    elif 'Trinidad' in item.attrib['v']:
                        city = 'Trinidad'
                    else:
                        city = item.attrib['v']
                    address[item.attrib['k'][5:]] = city
                else:                                       #add any other 'address' values as they are
                    address[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'name:' values in 'name' and remove 'name:' from key
            elif item.attrib['k'][:5]== 'name:':
                name[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'gnis:' values in 'gnis' and remove 'gnis:' from key
            elif item.attrib['k'][:5]== 'gnis:':
                gnis[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'tiger:' values in 'tiger' and remove 'tiger:' from key
            elif item.attrib['k'][:6]== 'tiger:':
                tiger[item.attrib['k'][6:]] = item.attrib['v']

            #nest 'alt_name:' values in 'alt_name' and remove 'alt_name:' from key
            elif item.attrib['k'][:9]== 'alt_name:':
                if item.attrib['k'] == 'is_in:state':       #Correct state abbreviations
                    if item.attrib['v'] == 'California':
                        alt_name[item.attrib['k'][9:]] = 'CA'
                    else:
                        alt_name[item.attrib['k'][9:]] = item.attrib['v']
                else:
                    alt_name[item.attrib['k'][9:]] = item.attrib['v']

            #nest 'caltrans:' values in 'caltrans' and remove 'caltrans:' from key
            elif item.attrib['k'][:9]== 'caltrans:':
                caltrans[item.attrib['k'][9:]] = item.attrib['v']

            #nest 'nhd:' values in 'nhd' and remove 'nhd:' from key
            elif item.attrib['k'][:4]== 'nhd:':
                nhd[item.attrib['k'][4:]] = item.attrib['v']

            #nest 'county:' values in 'county' and remove 'county:' from key
            elif item.attrib['k'][:7]== 'county:':
                county[item.attrib['k'][7:]] = item.attrib['v']

            #nest 'FG:' values in 'fg' and remove 'FG:' from key
            elif item.attrib['k'][:3]== 'FG:':
                fg[item.attrib['k'][3:]] = item.attrib['v']

            #nest 'csp:' values in 'csp' and remove 'csp:' from key
            elif item.attrib['k'][:4]== 'csp:':
                csp[item.attrib['k'][4:]] = item.attrib['v']

            #nest 'ref:' values in 'ref' and remove 'ref:' from key
            elif item.attrib['k'][:4]== 'ref:':
                ref[item.attrib['k'][4:]] = item.attrib['v']

            #nest 'flag:' values in 'flag' and remove 'flag:' from key
            elif item.attrib['k'][:5]== 'flag:':
                flag[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'old_name:' values in 'old_name' and remove 'old_name:' from key
            elif item.attrib['k'][:9]== 'old_name:':
                old_name[item.attrib['k'][9:]] = item.attrib['v']

            #nest 'fuel:' values in 'fuel' and remove 'fuel:' from key
            elif item.attrib['k'][:5]== 'fuel:':
                fuel[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'toilets:' values in 'toilets' and remove 'toilets:' from key
            elif item.attrib['k'][:8]== 'toilets:':
                toilets[item.attrib['k'][8:]] = item.attrib['v']

            #nest 'monitoring:' values in 'monitoring' and remove 'monitoring:' from key
            elif item.attrib['k'][:11]== 'monitoring:':
                monitoring[item.attrib['k'][11:]] = item.attrib['v']

            #nest 'oneway:' values in 'oneway' and remove 'oneway:' from key
            elif item.attrib['k'][:7]== 'oneway:':
                oneway[item.attrib['k'][7:]] = item.attrib['v']

            #nest 'lanes:' values in 'lanes' and remove 'lanes:' from key
            elif item.attrib['k'][:6]== 'lanes:':
                lanes[item.attrib['k'][6:]] = item.attrib['v']

            #nest 'turn:' values in 'turn' and remove 'turn:' from key
            elif item.attrib['k'][:5]== 'turn:':
                turn[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'park:' values in 'park' and remove 'park:' from key
            elif item.attrib['k'][:5]== 'park:':
                park[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'contact:' values in 'contact' and remove 'contact:' from key
            elif item.attrib['k'][:8]== 'contact:':
                contact[item.attrib['k'][8:]] = item.attrib['v']

            #nest 'hgv:' values in 'hgv' and remove 'hgv:' from key
            elif item.attrib['k'][:4]== 'hgv:':
                hgv[item.attrib['k'][4:]] = item.attrib['v']

            #nest 'diet:' values in 'diet' and remove 'diet:' from key
            elif item.attrib['k'][:5]== 'diet:':
                diet[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'boundary:' values in 'boundary' and remove 'boundary:' from key
            elif item.attrib['k'][:9]== 'boundary:':
                boundary[item.attrib['k'][9:]] = item.attrib['v']

            #nest 'payment:' values in 'payment' and remove 'payment:' from key
            elif item.attrib['k'][:8]== 'payment:':
                payment[item.attrib['k'][8:]] = item.attrib['v']

            #nest 'census:' values in 'census' and remove 'census:' from key
            elif item.attrib['k'][:7]== 'census:':
                census[item.attrib['k'][7:]] = item.attrib['v']

            #nest 'nist:' values in 'nist' and remove 'nist:' from key
            elif item.attrib['k'][:5]== 'nist:':
                nist[item.attrib['k'][5:]] = item.attrib['v']

            #nest 'internet_access:' values in 'internet_access' and remove 'internet_access:' from key
            elif item.attrib['k'][:16]== 'internet_access:':
                internet_access[item.attrib['k'][16:]] = item.attrib['v']

            #Fix values in specific tag fields
            elif item.attrib['k'] == 'type':    #Lowercase type (e.g. 'Public' to 'public')
                node[item.attrib['k']] = item.attrib['v'].lower()
            elif item.attrib['k'] == 'fax' or item.attrib['k'] == 'phone':
                numbers = item.attrib['v'].strip().replace(' ', '').replace('.', '').replace('-', '').replace('(', '').replace(')', '')[-10:]
                try:    #If numbers (actual phone number rather than 'Yes' or 'No' value), convert to international format
                    int(numbers)
                    node[item.attrib['k']] = '+1-' + numbers[0:3] + '-' + numbers[3:6] + '-' + numbers[6:]
                except:     #if not numbers, skip value
                    continue
            elif item.attrib['k'] == 'cuisine':     #Lowercase and format cuisine
                node[item.attrib['k']] = item.attrib['v'].lower().replace('_',  ' ').replace(', ', ';').replace(',', '').strip().replace(' ', '_')
            elif item.attrib['k'] == 'brand':       #Capitalize brand names
                node[item.attrib['k']] = item.attrib['v'].title()
            elif item.attrib['k'] == 'natural':     #Skip website URL found in 'natural'
                if item.attrib['v'] == 'http://baywestsupply.com/':
                    continue
                else:
                    node[item.attrib['k']] = item.attrib['v']
            elif item.attrib['k'] == 'route':   #Skip non access values in 'route'
                if item.attrib['v'] == '101' or item.attrib['v'] == '299':
                    continue
                else:
                    node[item.attrib['k']] = item.attrib['v']
            else:       #Put in as is if nothing special is specified for that key
                node[item.attrib['k']] = item.attrib['v']

        #Nest dictionaries if values found
        if len(address) > 0:
            node['address'] = address
        if len(name) > 0:
            node['name'] = name
        if len(gnis) > 0:
            node['gnis'] = gnis
        if len(tiger) > 0:
            node['tiger'] = tiger
        if len(alt_name) > 0:
            node['alt_name'] = alt_name
        if len(caltrans) > 0:
            node['caltrans'] = caltrans
        if len(nhd) > 0:
            node['nhd'] = nhd
        if len(county) > 0:
            node['county'] = county
        if len(fg) > 0:
            node['fg'] = fg
        if len(csp) > 0:
            node['csp'] = csp
        if len(ref) > 0:
            node['ref'] = ref
        if len(flag) > 0:
            node['flag'] = flag
        if len(old_name) > 0:
            node['old_name'] = old_name
        if len(fuel) > 0:
            node['fuel'] = fuel
        if len(toilets) > 0:
            node['toilets'] = toilets
        if len(monitoring) > 0:
            node['monitoring'] = monitoring
        if len(oneway) > 0:
            node['oneway'] = oneway
        if len(lanes) > 0:
            node['lanes'] = lanes
        if len(turn) > 0:
            node['turn'] = turn
        if len(park) > 0:
            node['park'] = park
        if len(contact) > 0:
            node['contact'] = contact
        if len(hgv) > 0:
            node['hgv'] = hgv
        if len(diet) > 0:
            node['diet'] = diet
        if len(boundary) > 0:
            node['boundary'] = boundary
        if len(payment) > 0:
            node['payment'] = payment
        if len(census) > 0:
            node['census'] = census
        if len(nist) > 0:
            node['nist'] = nist
        if len(internet_access) > 0:
            node['internet_access'] = internet_access

        #Return completed node
        return node
    else:
        return None

#Compile elements into list, write list to JSON file
def process_map(file_in):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)

        fo.write(json.dumps(data))

process_map(datafile)