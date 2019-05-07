import os
import json

thisfilepath = os.path.dirname(__file__)

global defaultsettingsdict
defaultsettingsdict = {'videosource': '/dev/video0'}

class settings(object):
    def __init__(self):
        settingsjsonpath = os.path.join(thisfilepath, 'rover_settings.json')
        self.dict = {}

        # create settings .json file (using defaultsettingsdict as a template) if it does not already exist
        if os.path.exists(settingsjsonpath) == False:
            with open(settingsjsonpath , 'w') as file:
                file.write(json.dumps(defaultsettingsdict))
                self.dict = defaultsettingsdict
        else:
            # .json file exists, load it:
            with open(settingsjsonpath, 'r') as file:
                self.dict = json.load(file)
  
