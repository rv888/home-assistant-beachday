"""Config flow for Beach Day."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .api import BeachDayApi, BeachDayApiError
from .const import API_BASE, CONF_BEACH_ID, DOMAIN


async def _validate(hass: HomeAssistant, api_key: str, beach_id: str) -> None:
    """Validate credentials and selected beach."""
    await BeachDayApi(api_key, API_BASE, beach_id).async_validate()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Beach Day."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                await _validate(self.hass, user_input[CONF_API_KEY], user_input[CONF_BEACH_ID])
            except BeachDayApiError:
                errors["base"] = "cannot_connect"
            except (ValueError, HomeAssistantError):
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(f"beach-{user_input[CONF_BEACH_ID]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Beach {user_input[CONF_BEACH_ID]}", data=user_input
                )

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_BEACH_ID): vol.Coerce(int),
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
