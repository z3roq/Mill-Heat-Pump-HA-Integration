import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode
from homeassistant.components.climate import ClimateEntityFeature
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
from .api import MillAPI
from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=1)
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    _LOGGER.info("Setting up Mill Heat Pump climate entities")
    email = entry.data["email"]
    password = entry.data["password"]
    api = MillAPI(email, password)


    houses = await hass.async_add_executor_job(api.get_houses)
    if not houses:
        _LOGGER.warning("No houses found for Mill Heat Pump account %s", email)
        return

    entities = []

    for house in houses:
        rooms = await hass.async_add_executor_job(api.get_rooms, house["id"])
        
        if not rooms:
            _LOGGER.warning("No rooms found for house %s", house.get("name"))
            continue
        for room in rooms:
            entities.append(MillRoomClimate(api, room))

    if entities:
        async_add_entities(entities, update_before_add=True)
    else:
        _LOGGER.warning("No climate entities to add")

class MillRoomClimate(ClimateEntity):

    def __init__(self, api, room):
        self._api = api
        self._room = room
        self._name = room.get("name", "Unknown Room")
        self._current_temperature = room.get("averageTemperature") or 0
        self._target_temperature = room.get("roomComfortTemperature") or 0
        self._attr_unique_id = room["id"]

        room_mode = room.get("mode")
        if room_mode == "comfort":
            self._hvac_mode = HVACMode.HEAT
        else:
            self._hvac_mode = HVACMode.OFF

    @property
    def name(self):
        return self._name

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def target_temperature_step(self):
        return 0.5  

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def hvac_modes(self):
        return [HVACMode.HEAT, HVACMode.OFF]

    @property
    def extra_state_attributes(self):
        return {
            "room_id": self._room["id"],
            "mode": self._room.get("mode"),
        }
    
    @property
    def supported_features(self):
        if self._hvac_mode == HVACMode.OFF:
            return ClimateEntityFeature(0)  
        return ClimateEntityFeature.TARGET_TEMPERATURE

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get("temperature")
        if temperature is not None:
            room_id = self._room["id"]
            await self.hass.async_add_executor_job(
                self._api.set_room_temperature, room_id, int(temperature)
            )
            await self.hass.async_add_executor_job(
                self._api.set_override_mode, room_id, "comfort"
            )

            self._target_temperature = int(temperature)
            self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        room_id = self._room["id"]

        if hvac_mode == HVACMode.HEAT:
            await self.hass.async_add_executor_job(
                self._api.set_override_mode, room_id, "comfort"
            )
            self._hvac_mode = HVACMode.HEAT

        elif hvac_mode == HVACMode.OFF:
            await self.hass.async_add_executor_job(
                self._api.set_override_mode, room_id, "off"
            )
            self._hvac_mode = HVACMode.OFF

        self.async_write_ha_state()
        
    async def async_update(self):

        house_id = self._room.get("houseId")
        rooms = await self.hass.async_add_executor_job(
            self._api.get_rooms, house_id
        )
        for r in rooms:
            if r["id"] == self._room["id"]:
                self._current_temperature = r.get("averageTemperature") or 0
                self._target_temperature = r.get("roomComfortTemperature") or 0
                if r.get("mode") == "comfort":
                    self._hvac_mode = HVACMode.HEAT
                else:
                    self._hvac_mode = HVACMode.OFF
                break
