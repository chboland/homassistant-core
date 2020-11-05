"""Platform for sensor integration."""
from homeassistant.components.waterkotte import WaterkotteApi
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from . import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    print("async_setup_entry(sensor.py)")
    api = hass.data[DOMAIN].get(config_entry.entry_id)
    entities = [WaterkotteSensor(api)]
    async_add_entities(entities, True)


class WaterkotteSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, api: WaterkotteApi):
        """Initialize the sensor."""
        self._state = None
        self._api = api

    @property
    def name(self):
        return "Outside Temperature"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._api.read_value("anyval")