Very primitive integration for Mill heat pump to Home Assistant.
Because heat pump cannot be directly controlled via API, this is workaround that controls the room, not heat pump directly. 

You loose ability to control pump from remote control after adding it to room. 

Instructions:

1. You need to have heat pump added to room in your Mill Nowrway app. Otherwise this wont work.

2. Copy custom_components content to your corresponding folder in HA

3. Go to Settings > Devices & services > Add integration and provide login credentials to Mill Norway App.

4. There should be now a climate entity named after room name in app.
