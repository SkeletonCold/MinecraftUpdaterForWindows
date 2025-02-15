import os
import time
import shutil
import hashlib
import time
import subprocess
from subprocess import PIPE
from datetime import datetime
import logging
import requests

# CONFIGURATION
UPDATE_TO_SNAPSHOT = False
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
BACKUP_DIR = 'world_backups'
JARBACKUP_DIR = 'previous_jars'
LOG_FILENAME = 'Update_Log.log'


logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# retrieve version manifest
response = requests.get(MANIFEST_URL)
data = response.json()

if UPDATE_TO_SNAPSHOT:
    minecraft_ver = data['latest']['snapshot']
else:
    minecraft_ver = data['latest']['release']

# get checksum of running server
if os.path.exists('server.jar'):
    sha = hashlib.sha1()
    f = open("server.jar", 'rb')
    sha.update(f.read())
    cur_ver = sha.hexdigest()
else:
    cur_ver = ""

for version in data['versions']:
    if version['id'] == minecraft_ver:
        jsonlink = version['url']
        jar_data = requests.get(jsonlink).json()
        jar_sha = jar_data['downloads']['server']['sha1']

        
        if cur_ver != jar_sha:
            logging.info('Update Found.')
            print('==============================================================================')
            print('Update Found.')
            print()
            logging.info('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)
            print('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)
            print('==============================================================================')
            time.sleep(1)
            logging.info('Updating server...')
            print('Updating server...')
            time.sleep(3)
        
            # logging.info('Stopping server.')
            # print('Stopping server.')
            # time.sleep(3)
            # os.system("TASKKILL /F /IM java.exe")
            time.sleep(1)
            
            if not os.path.exists(JARBACKUP_DIR):
                os.makedirs(JARBACKUP_DIR)

            backupPath2 = os.path.join(
                JARBACKUP_DIR,
                "minecraft_server_sha=" + cur_ver + ".jar")
            shutil.copy("server.jar", backupPath2)
            time.sleep(2)
            
            link = jar_data['downloads']['server']['url']
            logging.info('Downloading server_' + str(minecraft_ver)+'.jar from ' + link + '...')
            print('Downloading server_' + str(minecraft_ver)+'.jar from ' + link + '...')
            response = requests.get(link)
            time.sleep(5)
            with open('server.jar', 'wb') as jar_file:
                jar_file.write(response.content)
            logging.info('Downloaded.')
            print('Downloaded.')
            time.sleep(1)
            
            # logging.info('Backing up world...')
            # print('Backing up world...')

            # if not os.path.exists(BACKUP_DIR):
            #     os.makedirs(BACKUP_DIR)

            # backupPath = os.path.join(
            #     BACKUP_DIR,
            #     "world" + "_backup_" + datetime.now().isoformat().replace(':', '-') + "_sha=" + cur_ver)
            # shutil.copytree("world", backupPath)
            
            # time.sleep(1)
            # logging.info('Backed up world.')
            # print('Backed up world.')
            # time.sleep(1)
            
            # logging.info('Starting server...')
            # print('Starting server...')
            # logging.info('==============================================================================')
            # time.sleep(1)
            # os.system('start call Manual_Run.bat')
        else:
            print("Server Isn't running or Server is already up to date.")
            print('Latest version is ' + str(minecraft_ver))
            time.sleep(5)
        break

