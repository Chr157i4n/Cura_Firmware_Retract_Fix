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


#import ctypes  # An included library with Python install.  
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
                #ctypes.windll.user32.MessageBoxW(0, str(layer_Index), "layer_Index", 1)
                
                for line in lines:
                    
                    
                    TX_line_Index = lines.index(line)
                                        
                    if (line.startswith("T")):                    #Search for T0,T1,T2...
                         if (line[1].isdigit()):
                            #found Toolchange, only react if G10 is in the next ten lines
                            newTool=int(line[1])    #save new tool
                            lines.remove(line)      #delete toolchange line
                            
                            for line2 in lines:
                                G10_line_Index = lines.index(line2)
                                #ctypes.windll.user32.MessageBoxW(0, "newTool_Line " + str(TX_line_Index) + "    G10_line_Index " + str(G10_line_Index), "G10_line_Index", 1)
                                
                                if (    (line2.startswith("G10")) and (G10_line_Index>TX_line_Index) and (G10_line_Index<TX_line_Index+20)   ):
                                    
                                    lines.remove(line2)
                                    line="G10 S1\nT"+str(newTool)
                                    lines.insert(G10_line_Index,line)
                                    changed=True
                                    break

                    if (changed==True):
                        changed=False
                        break
                
                
                                        
                   
                result = "\n".join(lines)
                data[layer_Index] = result

            
        return data
