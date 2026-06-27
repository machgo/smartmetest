from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, METER_ENERGY_TYPE_NAMES
from .coordinator import SmartMeDataUpdateCoordinator


@dataclass(frozen=True, kw_only=True)
class SmartMeSensorEntityDescription(SensorEntityDescription):
    # Name of the API field that contains the unit for this measurement
    unit_key: str | None = None
    # Optional transform applied to the raw API value
    value_fn: Callable[[float], float] | None = None


SENSOR_DESCRIPTIONS: tuple[SmartMeSensorEntityDescription, ...] = (
    # --- Energy / counter readings ---
    SmartMeSensorEntityDescription(
        key="counterReading",
        name="Energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    SmartMeSensorEntityDescription(
        key="counterReadingT1",
        name="Energy Tariff 1",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    SmartMeSensorEntityDescription(
        key="counterReadingT2",
        name="Energy Tariff 2",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    SmartMeSensorEntityDescription(
        key="counterReadingT3",
        name="Energy Tariff 3",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    SmartMeSensorEntityDescription(
        key="counterReadingT4",
        name="Energy Tariff 4",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    SmartMeSensorEntityDescription(
        key="counterReadingImport",
        name="Energy Import",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    SmartMeSensorEntityDescription(
        key="counterReadingExport",
        name="Energy Export",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        unit_key="counterReadingUnit",
    ),
    # --- Power ---
    SmartMeSensorEntityDescription(
        key="activePower",
        name="Power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit_key="activePowerUnit",
    ),
    SmartMeSensorEntityDescription(
        key="activePowerL1",
        name="Power L1",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit_key="activePowerUnit",
    ),
    SmartMeSensorEntityDescription(
        key="activePowerL2",
        name="Power L2",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit_key="activePowerUnit",
    ),
    SmartMeSensorEntityDescription(
        key="activePowerL3",
        name="Power L3",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        unit_key="activePowerUnit",
    ),
    # --- Voltage ---
    SmartMeSensorEntityDescription(
        key="voltage",
        name="Voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SmartMeSensorEntityDescription(
        key="voltageL1",
        name="Voltage L1",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SmartMeSensorEntityDescription(
        key="voltageL2",
        name="Voltage L2",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SmartMeSensorEntityDescription(
        key="voltageL3",
        name="Voltage L3",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    # --- Current ---
    SmartMeSensorEntityDescription(
        key="current",
        name="Current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SmartMeSensorEntityDescription(
        key="currentL1",
        name="Current L1",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SmartMeSensorEntityDescription(
        key="currentL2",
        name="Current L2",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SmartMeSensorEntityDescription(
        key="currentL3",
        name="Current L3",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    # --- Power factor — API returns 0–1, HA expects % ---
    SmartMeSensorEntityDescription(
        key="powerFactor",
        name="Power Factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda v: round(v * 100, 1),
    ),
    SmartMeSensorEntityDescription(
        key="powerFactorL1",
        name="Power Factor L1",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda v: round(v * 100, 1),
    ),
    SmartMeSensorEntityDescription(
        key="powerFactorL2",
        name="Power Factor L2",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda v: round(v * 100, 1),
    ),
    SmartMeSensorEntityDescription(
        key="powerFactorL3",
        name="Power Factor L3",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda v: round(v * 100, 1),
    ),
    # --- Temperature ---
    SmartMeSensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    # --- Flow rate (water / gas meters) ---
    SmartMeSensorEntityDescription(
        key="flowRate",
        name="Flow Rate",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SmartMeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SmartMeSensorEntity] = [
        SmartMeSensorEntity(coordinator, device["id"], description)
        for device in coordinator.data
        for description in SENSOR_DESCRIPTIONS
        if device.get(description.key) is not None
    ]
    async_add_entities(entities)


class SmartMeSensorEntity(
    CoordinatorEntity[SmartMeDataUpdateCoordinator], SensorEntity
):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SmartMeDataUpdateCoordinator,
        device_id: str,
        description: SmartMeSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description: SmartMeSensorEntityDescription = description
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def _device_data(self) -> dict[str, Any]:
        for device in self.coordinator.data:
            if device["id"] == self._device_id:
                return device
        return {}

    @property
    def device_info(self) -> DeviceInfo:
        data = self._device_data
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=data.get("name") or f"Smart-me {self._device_id}",
            manufacturer="Smart-me",
            model=METER_ENERGY_TYPE_NAMES.get(
                data.get("deviceEnergyType", 0), "Unknown"
            ),
            serial_number=str(data["serial"]) if data.get("serial") else None,
        )

    @property
    def native_value(self) -> float | None:
        value = self._device_data.get(self.entity_description.key)
        if value is None:
            return None
        if self.entity_description.value_fn is not None:
            return self.entity_description.value_fn(value)
        return value

    @property
    def native_unit_of_measurement(self) -> str | None:
        if self.entity_description.unit_key:
            return self._device_data.get(self.entity_description.unit_key)
        return self.entity_description.native_unit_of_measurement
