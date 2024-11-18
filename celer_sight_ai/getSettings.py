import sys

import os

if hasattr(sys, "frozen"):
    sys.path = [str(os.environ["CELER_SIGHT_AI_HOME"])]
## Config file

import json
import os

# # APP SETTINGS
# class settingsObj(object):
#     # APP PATH
#     json_file = "extrPack/settingsApp.json"
#     app_path = os.path.abspath(os.getcwd())
#     settings_path = os.path.join(app_path, json_file)

#     def __init__(self):
#         self.deserialize()
#         self.settingsToAttributes(self.mySettings)

#     def settingsToAttributes(self, dictIn=None):
#         self.maxImageResImport_X = dictIn["maxImageResImport_X"]
#         self.maxImageResImport_Y = dictIn["maxImageResImport_Y"]
#         self.maxImageResResize_X = dictIn["maxImageResResize_X"]
#         self.maxImageResResize_Y = dictIn["maxImageResResize_Y"]
#         self.PolyColor_1 = dictIn["PolyColor_1"]
#         self.PolyOpacity_1 = dictIn["PolyOpacity_1"]
#         self.PolyCircleSize_1 = dictIn["PolyCircleSize_1"]
#         self.PolyWidth_1 = dictIn["PolyWidth_1"]
#         self.MagicBrushSize = dictIn["MagicBrushSize"]
#         self.MagicSkeletonRadius = dictIn["MagicSkeletonRadius"]
#         self.MagicSkeletonColor = dictIn["MagicSkeletonColor"]
#         self.MagicSkeletonOpacity = dictIn["MagicSkeletonOpacity"]
#         self.LastUsedEntity = dictIn["LastUsedEntity"]
#         self.AutoLogIn = dictIn["AutoLogIn"]
#         self.prev_cel_network = dictIn["prev_cel_network"]
#         self.prev_cel_analysis = dictIn["prev_cel_analysis"]

#     # DESERIALIZE JSON
#     def deserialize(self):
#         # READ JSON FILE
#         with open(self.settings_path, "r", encoding="utf-8") as reader:
#             self.mySettings = json.loads(reader.read())


# global settings
# settings = settingsObj()
