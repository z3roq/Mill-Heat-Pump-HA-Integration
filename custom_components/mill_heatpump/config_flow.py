import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .const import DOMAIN
from .api import MillAPI

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
})

class MillHeatPumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            api = MillAPI(email, password)
            try:
                await self.hass.async_add_executor_job(api.authenticate)
                houses = await self.hass.async_add_executor_job(api.get_houses)
                if not houses.get("ownHouses"):
                    errors["base"] = "no_houses"
                else:
                    return self.async_create_entry(
                        title=f"Mill Heat Pump ({email})",
                        data={CONF_EMAIL: email, CONF_PASSWORD: password},
                    )
            except Exception:
                errors["base"] = "auth"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
