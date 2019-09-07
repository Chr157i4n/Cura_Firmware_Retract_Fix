# Cura_Firmware_Retract_Fix
this postprocessing script fixes a problem, so that firmware rectract can be used with Cura

Cura has a hidden setting to use firmware retract.

Then it set G10 and G11 instead of G1 command to retract and recover.
This is for changing the retract setting in the printer, while printing.

Unfortunately Cura is not made for Multiple Extruder Single Nozzle Setups.

If there is a toolchange, the firmware retract should be used like this:

G10 S1
T1
G11

Cura writes the G-Code like this:

T1
G10
G11

The S1 is needed, that the printer knows, that it is a toolchange retract.

this postprocessing script changes the position of the G10 and the T1 and adds the S1 to the G10.
