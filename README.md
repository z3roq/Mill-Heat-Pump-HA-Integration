<h1>Mill Heat Pump Integration To Home Assistant</h1>
Very primitive integration for Mill heat pump to Home Assistant.
Because heat pump cannot be directly controlled via API because lack of support for some reason, this is workaround that controls the room, not heat pump directly. 

You lose ability to control pump from remote control after adding it to room. Also you need to choose from app if You want to heat or cool. Currently only implemented for heating purposes (have not even tried cooling), but cooling is on TODO list (maybe closer to summer).

<h3>Instructions:</h3>

1. You need to have heat pump added to room in your Mill Nowrway app. Otherwise this wont work.

2. Copy custom_components content to your corresponding folder in HA

3. Go to Settings > Devices & services > Add integration > Mill HeatPump and provide login credentials to Mill Norway App.

4. There should be now a climate entity named after room name in Home Assistant.

<h4>Note:</h4>
I am nowhere near of even basic developer, so there could be issues whit this. 

<h3>TODO:</h3>
<li>HACS installation</li>
<li>Check cooling stuff</li>
<li>Comment code</li>
<li>Make rooms as devices, not only entities</li>
