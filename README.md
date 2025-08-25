Very primitive integration for Mill heat pump to Home Assistant.
Because heat pump cannot be directly controlled via API because lack of support for some reason, this is workaround that controls the room, not heat pump directly. 

You lose ability to control pump from remote control after adding it to room. Also you need to choose from app if You want to heat or cool. Currently only implemented for heating purposes (have not even tried cooling), but cooling is on TODO list (maybe closer to summer lol).

Instructions:

1. You need to have heat pump added to room in your Mill Nowrway app. Otherwise this wont work.

2. Copy custom_components content to your corresponding folder in HA

3. Go to Settings > Devices & services > Add integration > Mill HeatPump and provide login credentials to Mill Norway App.

4. There should be now a climate entity named after room name in app.

Note:
I am nowhere near of even basic developer and this was done heavely relied on AI, so there could be issues whit this. 
