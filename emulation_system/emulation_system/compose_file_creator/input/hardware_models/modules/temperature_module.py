"""Model and attributes for Temperature Module."""
from typing import ClassVar, List, Optional

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
    TemperatureModelSettings,
)

from ..hardware_specific_attributes import HardwareSpecificAttributes
from .module_model import FirmwareSerialNumberModel, ModuleInputModel, ProxyInfoModel


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Temperature Module."""

    temperature: TemperatureModelSettings = TemperatureModelSettings()


class TemperatureModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class TemperatureModuleInputModel(ModuleInputModel):
    """Model for Temperature Module."""

    firmware_serial_number_info: ClassVar[
        FirmwareSerialNumberModel
    ] = FirmwareSerialNumberModel(
        model="temp_deck_v20", version="v2.0.1", env_var_name="OT_EMULATOR_tempdeck"
    )
    proxy_info: ClassVar[ProxyInfoModel] = ProxyInfoModel(
        env_var_name="OT_EMULATOR_temperature_proxy",
        emulator_port=10001,
        driver_port=11001,
    )

    hardware: Literal[Hardware.TEMPERATURE_MODULE]
    source_repos: TemperatureModuleSourceRepositories = Field(
        default=TemperatureModuleSourceRepositories(), const=True, exclude=True
    )
    hardware_specific_attributes: TemperatureModuleAttributes = Field(
        default=TemperatureModuleAttributes()
    )

    emulation_level: Literal[EmulationLevels.FIRMWARE]

    def get_firmware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return [emulator_proxy_name]
