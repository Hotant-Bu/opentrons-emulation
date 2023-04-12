"""Module containing logic for e2e tests."""
from dataclasses import dataclass, field

from tests.e2e.fixtures.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.fixtures.module_containers import ModuleContainers
from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.consts import (
    CommonMounts,
    ModulesExpectedBinaryNames,
    MonorepoBuilderNamedVolumes,
    OpentronsModulesBuilderNamedVolumes,
    OpentronsModulesEmulatorNamedVolumes,
    OT3FirmwareBuilderNamedVolumes,
    OT3FirmwareExpectedBinaryNames,
)
from tests.e2e.utilities.helper_functions import (
    confirm_mount_does_not_exist,
    confirm_mount_exists,
    confirm_named_volume_exists,
    exec_in_container,
)
from tests.e2e.utilities.results.e2e_test_output import E2ETestOutput
from tests.e2e.utilities.results.results import (
    OT3EmulatorContainers,
    Result,
)
from tests.e2e.utilities.results.single_test_description import TestDescription


@dataclass
class SystemTestDefinition:
    """Class representing expected results for a specific yaml configuration file."""

    test_id: str
    yaml_config_relative_path: str
    monorepo_builder_created: bool
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool

    local_monorepo_mounted: bool
    local_ot3_firmware_mounted: bool
    local_opentrons_modules_mounted: bool

    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations
    _test_output: E2ETestOutput = field(
        init=False, repr=False, compare=False, default=E2ETestOutput()
    )

    def _confirm_entrypoint_mounts(
        self, ot3_system: OT3SystemUnderTest, modules: ModuleContainers
    ) -> None:
        containers = ot3_system.containers_with_entrypoint_script + modules.all_modules
        for container in containers:
            expected_mount = CommonMounts.ENTRYPOINT_MOUNT
            test_description = TestDescription.from_mount(container, expected_mount)
            self._test_output.append_result(
                confirm_mount_exists(container, CommonMounts.ENTRYPOINT_MOUNT),
                test_description,
            )

    def _confirm_ot3_firmware_builder_named_volumes(
        self, ot3_system: OT3SystemUnderTest
    ) -> None:
        for volume in OT3FirmwareBuilderNamedVolumes.VOLUMES:
            test_description = TestDescription.from_named_volume(
                ot3_system.firmware_builder, volume
            )
            self._test_output.append_result(
                confirm_named_volume_exists(ot3_system.firmware_builder, volume),
                test_description,
            )


    def _confirm_containers_with_monorepo_wheel_volumes(
        self, ot3_system: OT3SystemUnderTest, modules: ModuleContainers
    ) -> None:
        containers = (
            ot3_system.containers_with_monorepo_wheel_volume
            + modules.firmware_level_modules
        )
        for container in containers:
            for expected_volume in MonorepoBuilderNamedVolumes.VOLUMES:
                test_description = TestDescription.from_named_volume(
                    container, expected_volume
                )
                self._test_output.append_result(
                    confirm_named_volume_exists(container, expected_volume),
                    test_description,
                )

    def _confirm_opentrons_modules_builder_named_volumes(
        self, ot3_system: OT3SystemUnderTest
    ) -> None:
        for volume in OpentronsModulesBuilderNamedVolumes.VOLUMES:
            test_description = TestDescription.from_named_volume(
                ot3_system.modules_builder, volume
            )
            self._test_output.append_result(
                confirm_named_volume_exists(ot3_system.modules_builder, volume),
                test_description,
            )

    def _confirm_opentrons_modules_emulator_named_volumes(
        self, modules: ModuleContainers
    ) -> None:
        heater_shaker_hardware_volume = (
            OpentronsModulesEmulatorNamedVolumes.HEATER_SHAKER
        )
        thermocycler_hardware_volume = OpentronsModulesEmulatorNamedVolumes.THERMOCYCLER
        if len(modules.hardware_emulation_heater_shaker_modules) > 0:
            for heater_shaker in modules.hardware_emulation_heater_shaker_modules:
                test_description = TestDescription.from_named_volume(
                    heater_shaker, heater_shaker_hardware_volume
                )
                self._test_output.append_result(
                    confirm_named_volume_exists(
                        heater_shaker, heater_shaker_hardware_volume
                    ),
                    test_description,
                )
        if len(modules.hardware_emulation_thermocycler_modules) > 0:
            for thermocycler in modules.hardware_emulation_thermocycler_modules:
                test_description = TestDescription.from_named_volume(
                    thermocycler, thermocycler_hardware_volume
                )
                self._test_output.append_result(
                    confirm_named_volume_exists(
                        thermocycler, thermocycler_hardware_volume
                    ),
                    test_description,
                )

    def _confirm_ot3_firmware_build_artifacts(self, ot3_system: OT3SystemUnderTest) -> None:
        test_matrix = (
            (ot3_system.gantry_x, OT3FirmwareExpectedBinaryNames.GANTRY_X),
            (ot3_system.gantry_y, OT3FirmwareExpectedBinaryNames.GANTRY_Y),
            (ot3_system.head, OT3FirmwareExpectedBinaryNames.HEAD),
            (ot3_system.gripper, OT3FirmwareExpectedBinaryNames.GRIPPER),
            (ot3_system.pipettes, OT3FirmwareExpectedBinaryNames.PIPETTES),
            (ot3_system.bootloader, OT3FirmwareExpectedBinaryNames.BOOTLOADER),
        )
        for container, expected_sim_name in test_matrix:
            test_description = TestDescription(
                f"Confirming container {container.name} has simulator binary inside of /executable"
            )
            self._test_output.append_result(
                exec_in_container(container, "ls /executable") == expected_sim_name,
                test_description,
            )

    def _confirm_opentrons_modules_build_artifacts(
        self, modules: ModuleContainers
    ) -> None:
        test_matrix = (
            (
                modules.hardware_emulation_thermocycler_modules,
                ModulesExpectedBinaryNames.THERMOCYCLER,
            ),
            (
                modules.hardware_emulation_heater_shaker_modules,
                ModulesExpectedBinaryNames.HEATER_SHAKER,
            ),
        )
        for container_list, expected_sim_name in test_matrix:
            if len(container_list) > 0:
                for container in container_list:
                    test_description = TestDescription(
                        f"Confirming container {container.name} has simulator binary named {expected_sim_name} inside of /executable"
                    )
                    self._test_output.append_result(
                        exec_in_container(container, "ls /executable")
                        == expected_sim_name,
                        test_description,
                    )

    def is_failure(self) -> bool:
        """Public facing method to expose whether any test cases failed."""
        return self._test_output.is_failure

    def print_output(self) -> str:
        """Public facing method to print output of test."""
        return self._test_output.get_results()

    def compare(
        self,
        ot3_system: OT3SystemUnderTest,
        modules: ModuleContainers,
        mounts: ExpectedBindMounts,
    ) -> None:
        """Public facing method to run all above protected assertion methods."""
        self._confirm_created_builders(ot3_system)
        self._confirm_local_mounts(ot3_system)
        self._confirm_build_args(ot3_system)
        self._confirm_entrypoint_mounts(ot3_system, modules)

        if self.monorepo_builder_created:
            test_description = TestDescription.from_mount(
                ot3_system.monorepo_builder,
                CommonMounts.ENTRYPOINT_MOUNT,
                confirm_not_exists=True,
            )
            self._test_output.append_result(
                confirm_mount_does_not_exist(
                    ot3_system.monorepo_builder, CommonMounts.ENTRYPOINT_MOUNT
                ),
                test_description,
            )

            self._confirm_containers_with_monorepo_wheel_volumes(ot3_system, modules)

        if self.ot3_firmware_builder_created:
            test_description = TestDescription.from_mount(
                ot3_system.firmware_builder,
                CommonMounts.ENTRYPOINT_MOUNT,
                confirm_not_exists=True,
            )
            self._test_output.append_result(
                confirm_mount_does_not_exist(
                    ot3_system.firmware_builder, CommonMounts.ENTRYPOINT_MOUNT
                ),
                test_description,
            )

            self._confirm_ot3_emulator_named_volumes(ot3_system)
            self._confirm_ot3_firmware_builder_named_volumes(ot3_system)
            self._confirm_ot3_firmware_state_manager_mounts_and_volumes(ot3_system)
            self._confirm_ot3_firmware_build_artifacts(ot3_system)

        if self.opentrons_modules_builder_created:
            test_description = TestDescription.from_mount(
                ot3_system.modules_builder,
                CommonMounts.ENTRYPOINT_MOUNT,
                confirm_not_exists=True,
            )
            self._test_output.append_result(
                confirm_mount_does_not_exist(
                    ot3_system.modules_builder, CommonMounts.ENTRYPOINT_MOUNT
                ),
                test_description,
            )
            self._confirm_opentrons_modules_builder_named_volumes(ot3_system)
            self._confirm_opentrons_modules_emulator_named_volumes(modules)
            self._confirm_opentrons_modules_build_artifacts(modules)

        if (
            self.local_monorepo_mounted
            and self.monorepo_builder_created
            and mounts.MONOREPO is not None
        ):
            test_description = TestDescription.from_mount(
                ot3_system.monorepo_builder, mounts.MONOREPO
            )

            self._test_output.append_result(
                confirm_mount_exists(ot3_system.monorepo_builder, mounts.MONOREPO),
                test_description,
            )

        if (
            self.local_ot3_firmware_mounted
            and self.ot3_firmware_builder_created
            and mounts.FIRMWARE is not None
        ):
            test_description = TestDescription.from_mount(
                ot3_system.firmware_builder, mounts.FIRMWARE
            )

            self._test_output.append_result(
                confirm_mount_exists(ot3_system.firmware_builder, mounts.FIRMWARE),
                test_description,
            )

        if (
            self.local_opentrons_modules_mounted
            and self.opentrons_modules_builder_created
            and mounts.MODULES is not None
        ):
            test_description = TestDescription.from_mount(
                ot3_system.modules_builder, mounts.MODULES
            )

            self._test_output.append_result(
                confirm_mount_exists(ot3_system.modules_builder, mounts.MODULES),
                test_description,
            )

        def generate_expected_results(self) -> Result:
            if self.ot3_firmware_builder_created:
                OT3EmulatorContainers()
