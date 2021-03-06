import requests
import sys
import getpass
import json
import configparser
from firebase import firebase
config = {}
with open('config.json', 'r') as f:
    config = json.load(f)

firebaseEndpoint = config["DEFAULT"]["firebase_endpoint"]
firebase = firebase.FirebaseApplication(firebaseEndpoint, None)
github = 'https://api.github.com/'
user = ''
pw = ''
dataObj = {}

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    print('[%s] %s%s ...%s' % (bar, percents, '%', status), end='\r')
    sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

def processRepoData( data ):
    dataLength = len(data["items"])
    numOut = 0
    for element in data["items"]:
        num = 0
        repUrl = element["repos_url"]
        repoData = getRepoData( repUrl )
        repoLength = len(repoData)
        for repo in repoData:
            getAndPostRepoLanguageData(repo["owner"]["login"], repo["name"])
            num = num + 1
            strang = "Inspecting Code of repositories of user " + str(numOut)
            progress(num, repoLength, strang)
        numOut = numOut + 1
    return

def getRepoData( repUrl ):
    PARAMS = {'Content-Type':'application/json'}
    r = requests.get(url = repUrl, params = PARAMS, auth =( user, pw ))
    return r.json()

def getAndPostRepoLanguageData(owner, name):
    langUrl = github + 'repos/' + owner + '/' + name +'/languages'
    PARAMS = {'Content-Type':'application/json'}
    r = requests.get(url = langUrl, params = PARAMS, auth =( user, pw ))
    object = r.json()
    checkIfLangInArrayAndConstruct(dataObj, object)
    return

def checkIfLangInArrayAndConstruct(arr, obj):
    for (k, v) in obj.items():
       if containsLang(dataObj, k) is False:
           dataObj[k] = v
           #Insert key into json obj and set value
       if containsLang(dataObj, k) is True:
           dataObj[k] = dataObj[k] + v
           #Find key and add to value

def containsLang(obj, key):
    if key in obj:
        return True
    return False

user = input('Enter in Github username (or skip for limited querires): ')
if user != '':
    pw = getpass.getpass('Enter in Github password: ')

print('Number of endpoints to query = ', (len(sys.argv) - 1), '\nBeginning given requests...\n')
for i, endpoint in enumerate(sys.argv):
    if i > 0:
        URL = github + endpoint
        print('\nURL', i, ': ', URL)
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'Content-Type':'application/json'}
        # sending get request and saving the response as response object
        j = 0
        limit = 10
        prog = ''
        while j < limit:
            prog = str(j) + '/' + str(limit)
            print('Overall Progress:', prog, '\n\n')
            page = '&page=' + str(j)
            r = requests.get(url = URL + (page), params = PARAMS, auth =( user, pw ))
            contentType = r.headers['Content-Type'].split(';')
            if contentType[0] == 'application/json':
                data = r.json()
                processRepoData(data)
            j = j + 1
            prog = str(limit) + '/' + str(limit)
        print(dataObj)
        print("Posting shcraped data to db...")
        fireData = {'progLangs' : dataObj}
        sent = json.dumps(fireData)
        result = firebase.post(config["DEFAULT"]["firebase_collection"], sent)
print("Done!")
