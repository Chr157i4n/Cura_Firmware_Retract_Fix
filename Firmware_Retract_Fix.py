# Cura PostProcessingPlugin
# Author:   Christian Köhlke
# Date:     Septemper 07, 2019

# Description:  postprocessing-script for fixing Cura - Marlin Firmware retract
#
#
#       Original
#
#       T0
#       G10
#       G11
#
#
#       How it should be
#
#       G10 S1
#       T0
#       G11
#
#
#


import ctypes  # An included library with Python install.  
from ..Script import Script
from UM.Application import Application

class Firmware_Retract_Fix(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Firmware_Retract_Fix",
            "key": "Firmware_Retract_Fix",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "active":
                {
                    "label": "active",
                    "description": "active",
                    "type": "bool",
                    "default_value": true
                }

                
            }
        }"""

    def execute(self, data):
        
        active = self.getSettingValueByKey("active")
        if active:
            for layer in data:
                changed=False
                layer_Index = data.index(layer)
                lines = layer.split("\n")
                deletedLines=0


                IndicesG=[]
                IndicesG=[i for i in range(len(lines)) if (lines[i]=="G10")]
                
                #IndexT=[i for i in range(len(lines)) if ((lines[i][0]=="T") and (lines[i][1].isdigit()))]
                IndicesT=[]
                for i in range(len(lines)):
                    if lines[i]:
                        if ((lines[i][0]=="T") and (lines[i][1].isdigit())):
                            IndicesT.append(i)
                
                #got the Indices of all G10 and Toolchanges in one Layer

                for IndexT in IndicesT:
                    for IndexG in IndicesG:
                        if (IndexG>IndexT) and (IndexG<IndexT+20):
                            #Found toolchange with retract
                            #ctypes.windll.user32.MessageBoxW(0, "newTool-Line: "+str(lines[IndexT-deletedLines]) + " newTool: "+str(lines[IndexT-deletedLines][1]), "newTool", 1)
                            newTool=lines[IndexT-deletedLines][1]
                            
                            #ctypes.windll.user32.MessageBoxW(0, str(lines[IndexT-deletedLines-1])+"\n\n"+str(lines[IndexT-deletedLines])+"\n\n"+str(lines[IndexT-deletedLines+1]), "delete Line", 1)
                            lines.pop(IndexT-deletedLines)
                            deletedLines=deletedLines+1
                            
                            #ctypes.windll.user32.MessageBoxW(0, str(lines[IndexG-deletedLines-1])+"\n\n"+str(lines[IndexG-deletedLines])+"\n\n"+str(lines[IndexG-deletedLines+1]), "delete Line", 1)
                            lines.pop(IndexG-deletedLines)
                            deletedLines=deletedLines+1
                            
                            newLine="G10 S1\nT"+str(newTool)
                            
                            #ctypes.windll.user32.MessageBoxW(0, str(newLine), "insert Line", 1)
                            lines.insert(IndexG-deletedLines,newLine)
                            deletedLines=deletedLines-1
                            
                            
                
                #ctypes.windll.user32.MessageBoxW(0, str(IndexT), "IndexT", 1)
                result = "\n".join(lines)
                data[layer_Index] = result
        return data
