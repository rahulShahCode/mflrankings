from bs4 import BeautifulSoup
import requests 
import re 
# Links to grab html from
base = 'http://www.borischen.co/p/'
qb = 'quarterback-tier-rankings.html'
rb = 'ppr-running-back-tier-rankings.html'
wr = 'ppr-wide-receiver-tier-rankings.html'
te = 'blog-page.html'
k = 'kicker-tier-rankings.html'
dst = 'defense-dst-tier-rankings.html'
flex = 'all-data-are-from-fantasypros.html'

# Gets tier rankings for specified position
def getTiers(pos):
    html = requests.get(base + pos)
    soup = BeautifulSoup(html.text, 'html.parser')
    return requests.get((soup.find('object'))['data']).text

# Parses the full tier list 
def parse(str):
# Each line is read as:
# Tier N: First Last, Player Name .. 


data = getTiers(qb)
