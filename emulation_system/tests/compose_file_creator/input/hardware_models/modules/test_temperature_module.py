"""Tests for Temperature Module."""
from typing import (
    Any,
    Dict,
)

import pytest
from pydantic import (
    ValidationError,
    parse_obj_as,
)

from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    TemperatureModuleInputModel,
)
from tests.compose_file_creator.conftest import (
    TEMPERATURE_MODULE_EMULATION_LEVEL,
    TEMPERATURE_MODULE_ID,
    TEMPERATURE_MODULE_SOURCE_TYPE,
)


def test_default_temperature_module(temperature_module_default: Dict[str, Any]) -> None:
    """Confirm Temperature Module is parsed correctly and defaults are applied."""
    therm = parse_obj_as(TemperatureModuleInputModel, temperature_module_default)
    assert therm.hardware == Hardware.TEMPERATURE_MODULE.value
    assert therm.id == TEMPERATURE_MODULE_ID
    assert therm.emulation_level == TEMPERATURE_MODULE_EMULATION_LEVEL
    assert therm.source_type == TEMPERATURE_MODULE_SOURCE_TYPE
    assert therm.hardware_specific_attributes.temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.temperature.starting == 23.0


def test_temperature_module_with_temp(
    temperature_module_set_temp: Dict[str, Any]
) -> None:
    """Confirm Temperature Module is parsed correctly.

    Confirm user-defined settings are applied.
    """
    therm = parse_obj_as(TemperatureModuleInputModel, temperature_module_set_temp)
    assert therm.hardware == Hardware.TEMPERATURE_MODULE.value
    assert therm.id == TEMPERATURE_MODULE_ID
    assert therm.emulation_level == TEMPERATURE_MODULE_EMULATION_LEVEL
    assert therm.source_type == TEMPERATURE_MODULE_SOURCE_TYPE
    assert therm.hardware_specific_attributes.temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.temperature.starting == 20.0


def test_temperature_module_with_bad_emulation_level(
    temperature_module_bad_emulation_level: Dict[str, Any]
) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(
            TemperatureModuleInputModel, temperature_module_bad_emulation_level
        )


def test_temperature_module_source_repos(
    temperature_module_default: Dict[str, Any]
) -> None:
    """Confirm that defined source repos are correct."""
    temp = parse_obj_as(TemperatureModuleInputModel, temperature_module_default)
    assert temp.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert temp.source_repos.hardware_repo_name is None