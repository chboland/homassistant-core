"""The Waterkotte heatpump integration."""
import asyncio
from logging import log
import random

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    if DOMAIN not in config:
        return True

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    conf = entry.data
    waterkotteApi = WaterkotteApi(
        conf.get(CONF_HOST), conf.get(CONF_USERNAME), conf.get(CONF_PASSWORD)
    )
    hass.data.setdefault(DOMAIN, {}).update({entry.entry_id: waterkotteApi})

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class WaterkotteApi:
    def __init__(self, host: str, user: str, password: str):
        self._host = host
        self._user = user
        self._password = password

    def read_value(self, val):
        return random.random()
