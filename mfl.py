import requests
import xml.etree.ElementTree as ET 
import json 
import re 

### PARAMETERS ### 
league_id = '17792'
username = 'rahul9801'
password = '*******'
year = 2020
host = 'www68.myfantasyleague.com'
base_url = f'https://api.myfantasyleague.com/{year}/' 
url = f'https://{host}/{year}/export'


# Outputs to file, if no filename is specified, send content to 
# 'output.txt'
def write(text, filename=None): 
    f = None 
    if filename is None: f = open('output.txt', 'w')
    else: f = open(filename, 'w')
    f.write(text)

# Login to MFL and return the response cookie 
def login(username, password):
    login_url = base_url + \
    f'login?USERNAME={username}&PASSWORD={password}&XML=1'
    response = requests.post(login_url)
    cookie = ET.fromstring(response.text).attrib
    return cookie 

# Get data from MFL - currently free agents player ids only 
def get(url, header, request,  pos=""):
    args = f"?TYPE={request}&L={league_id}&POSITION={pos}&JSON=1"
    url += args 
    response = requests.get(url, header)
    if response.status_code == 200: 
        write(response.text, 'qb.json')
        return json.loads(response.text)
    else: print('Failed: ' + response.reason)

def format(name):
    pattern = '([\w\-\.\s]+),([\w\-\.\s]+)'
    m = re.match(pattern, name)
    return (m.group(2)[1:] + ' ' + m.group(1))
def to_lst(players, arg):
    lst = [] 
    if arg == 'name': 
        for player in players: lst.append(format(player[arg]))
    for player in players: lst.append(player[arg])
    return lst
def getNames(id_dict): 
    ids = to_lst(id_dict, 'id')
    id_str = ','.join(ids)
    response = requests.get(base_url + 'export', params={'TYPE': 'players', 
                            'PLAYERS': id_str,
                            'JSON': '1'})
    player_info = json.loads(response.text)['players']['player']
    names = to_lst(player_info, 'name')
    return names 

cookie = login(username, password)
ids = get(url, cookie, 'freeAgents', 'QB')['freeAgents']\
['leagueUnit']['player']
names = getNames(ids)