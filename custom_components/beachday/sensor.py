"""Sensors for Beach Day."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        BeachDaySensor(coordinator, entry, "score", "Beach Day Score", None),
        BeachDaySensor(coordinator, entry, "water_temperature", "Water Temperature", UnitOfTemperature.CELSIUS),
        BeachDaySensor(coordinator, entry, "air_temperature", "Air Temperature", UnitOfTemperature.CELSIUS),
    ])


def _nested_number(data: dict[str, Any], *keys: str) -> float | None:
    """Find a numeric value in condition blobs using common field names."""
    for section in ("weather", "ocean_conditions", "water_quality"):
        blob = data.get(section)
        if isinstance(blob, dict):
            for key in keys:
                value = blob.get(key)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    return value
    return None


class BeachDaySensor(CoordinatorEntity, SensorEntity):
    """A Beach Day measurement sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry, key: str, name: str, unit: str | None) -> None:
        super().__init__(coordinator)
        beach_id = entry.data["beach_id"]
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"beachday_{beach_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_has_entity_name = True

    @property
    def native_value(self):
        data = self.coordinator.data
        if self._key == "score":
            return data.get("beach_day_score")
        if self._key == "water_temperature":
            return _nested_number(data, "water_temperature", "temperature_c", "temp_c")
        return _nested_number(data, "air_temperature", "temperature", "temperature_c", "temp_c")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        return {key: value for key, value in data.items() if key in {"id", "name", "state", "country", "city", "latitude", "longitude"}}
