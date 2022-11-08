"""Functions for usage with HardwareModel objects."""
from typing import TypeGuard

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    SourceType,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    ModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    RobotInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)


def is_robot(hardware: HardwareModel) -> TypeGuard[RobotInputModel]:
    """Whether hardware is a robot."""
    return issubclass(hardware.__class__, RobotInputModel)


def is_module(hardware: HardwareModel) -> TypeGuard[ModuleInputModel]:
    """Whether hardware is a module."""
    return issubclass(hardware.__class__, ModuleInputModel)


def is_ot2(hardware: HardwareModel) -> TypeGuard[OT2InputModel]:
    """Whether hardware is an OT-2."""
    return isinstance(hardware, OT2InputModel)


def is_ot3(hardware: HardwareModel) -> TypeGuard[OT3InputModel]:
    """Whether hardware is an OT-3"""
    return isinstance(hardware, OT3InputModel)


def is_heater_shaker_module(
    hardware: HardwareModel,
) -> TypeGuard[HeaterShakerModuleInputModel]:
    """Whether hardware is a heater-shaker module."""
    return isinstance(hardware, HeaterShakerModuleInputModel)


def is_magnetic_module(hardware: HardwareModel) -> TypeGuard[MagneticModuleInputModel]:
    """Whether hardware is a magnetic module."""
    return isinstance(hardware, MagneticModuleInputModel)


def is_temperature_module(
    hardware: HardwareModel,
) -> TypeGuard[TemperatureModuleInputModel]:
    """Whether hardware is a temperature module."""
    return isinstance(hardware, TemperatureModuleInputModel)


def is_thermocycler_module(
    hardware: HardwareModel,
) -> TypeGuard[ThermocyclerModuleInputModel]:
    """Whether hardware is a thermocycler module."""
    return isinstance(hardware, ThermocyclerModuleInputModel)


def is_remote_robot(hardware: HardwareModel) -> TypeGuard[RobotInputModel]:
    """Whether hardware is a remote robot."""
    return (
        is_robot(hardware)
        and hasattr(hardware, "robot_server_source_type")
        and getattr(hardware, "robot_server_source_type") == SourceType.REMOTE
    )


def is_remote_module(hardware: HardwareModel) -> TypeGuard[ModuleInputModel]:
    """Whether hardware is a remote module."""
    return (
        is_module(hardware)
        and hasattr(hardware, "source_type")
        and getattr(hardware, "source_type") == SourceType.REMOTE
    )


def is_hardware_emulation_level(hardware: HardwareModel) -> bool:
    """Whether hardware is hardware emulation level."""
    return hardware.emulation_level == EmulationLevels.HARDWARE