"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""

from pydantic import Field

from emulation_system.compose_file_creator.images import get_image_name
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateEnvironmentVariables,
)

from ..hardware_model import HardwareModel


class RobotInputModel(HardwareModel):
    """Parent class of all Robots. Subclass of HardwareModel.

    Used to group all robots together and distinguish them from modules.
    """

    exposed_port: int = Field(default=31950)
    bound_port: int = Field(default=31950)

    robot_server_env_vars: IntermediateEnvironmentVariables | None
    emulator_proxy_env_vars: IntermediateEnvironmentVariables | None

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(self.hardware, self.emulation_level)
