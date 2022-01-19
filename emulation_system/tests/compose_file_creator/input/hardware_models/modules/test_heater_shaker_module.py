"""Tests for heater-shaker module."""
from typing import (
    Any,
    Dict,
)

import pytest
from pydantic import (
    ValidationError,
    parse_obj_as,
)

from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    HeaterShakerModes,
    OpentronsRepository,
)
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_EMULATION_LEVEL,
    HEATER_SHAKER_MODULE_ID,
    HEATER_SHAKER_MODULE_SOURCE_TYPE,
)


def test_default_heater_shaker(heater_shaker_module_default: Dict[str, Any]) -> None:
    """Confirm Heater-Shaker is parsed right and default mode of socket is set."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_module_default)
    assert hs.hardware == Hardware.HEATER_SHAKER_MODULE.value
    assert hs.id == HEATER_SHAKER_MODULE_ID
    assert hs.emulation_level == HEATER_SHAKER_MODULE_EMULATION_LEVEL
    assert hs.source_type == HEATER_SHAKER_MODULE_SOURCE_TYPE
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.SOCKET


def test_heater_shaker_with_stdin(
    heater_shaker_module_use_stdin: Dict[str, Any]
) -> None:
    """Confirm Heater-Shaker is parsed right and stdin mode is picked up."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_module_use_stdin)
    assert hs.hardware == Hardware.HEATER_SHAKER_MODULE.value
    assert hs.id == HEATER_SHAKER_MODULE_ID
    assert hs.emulation_level == HEATER_SHAKER_MODULE_EMULATION_LEVEL
    assert hs.source_type == HEATER_SHAKER_MODULE_SOURCE_TYPE
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.STDIN


def test_heater_shaker_with_bad_emulation_level(
    heater_shaker_module_bad_emulation_level: Dict[str, Any]
) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(
            HeaterShakerModuleInputModel, heater_shaker_module_bad_emulation_level
        )


def test_heater_shaker_source_repos(
    heater_shaker_module_default: Dict[str, Any]
) -> None:
    """Confirm that defined source repos are correct."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_module_default)
    assert hs.source_repos.firmware_repo_name is None
    assert hs.source_repos.hardware_repo_name == OpentronsRepository.OPENTRONS_MODULES