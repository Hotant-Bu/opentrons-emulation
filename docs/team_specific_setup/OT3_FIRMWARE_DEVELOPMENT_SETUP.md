# OT3 Firmware Development Setup Instructions

Below are the instructions for settings up an OT-3 robot-server emulator with your own local source.

### Requirements

This configuration requires that you have [the opentrons repo](https://github.com/Opentrons/opentrons) and
[the ot3-firmware repo](https://github.com/Opentrons/ot3-firmware) downloaded locally to your system.

### Initial Setup

Follow [these](https://github.com/Opentrons/opentrons-emulation/blob/main/README.md#initial-configuration) instructions.

### Modify Configuration file

Go into `samples/team_specific_setups/ot3_firmware_development.yaml` and replace the following values with paths to the
**_TOP_** level of your repos:

- `robot.source-location` - Absolute path to your `ot3-firmware` repo.
  - Example: `/home/derek-maggio/Documents/repos/ot3-firmware`
- `robot.robot-server-source-location` - Absolute path to your `opentrons` repo.
  - Example: `/home/derek-maggio/Documents/repos/opentrons`
- `robot.can-server-source-location` - Absolute path to your `opentrons` repo.
  - Example: `/home/derek-maggio/Documents/repos/opentrons`

Your configuration should look something like the following:

```yaml
system-unique-id: ot3-only
robot:
  id: otie
  hardware: ot3
  source-type: local
  source-location: /home/derek-maggio/Documents/repos/ot3-firmware
  robot-server-source-type: local
  robot-server-source-location: /home/derek-maggio/Documents/repos/opentrons
  can-server-source-type: local
  can-server-source-location: /home/derek-maggio/Documents/repos/opentrons
  emulation-level: hardware
  exposed-port: 31950
```

### Build Docker Images

From the root of the repo run

```
Intel: make build-amd64 file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
Mac M1: make build-arm64 file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

> This may take 10 or more minutes on initial build.

### Run Emulation then Build and Start OT3 Firmware Emulators

1. From the root of the repo run the following command to start the containers.

```shell
make run-detached file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

2. Then run the following command to run builds inside containers with source code mounted into them.

```shell
make local-rebuild-all file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

> Note: This second step is necessary because we bound our source code into the emulators. It is up to the user to execute the build and run of any containers they have their local source bound into.

> Note: There is a quiet version of the command `local-rebuild-all-quiet`

### Make Sure Emulation is Actually Working

1. Open 2 terminals
1. Run CAN monitoring script in the first terminal

```shell
make can-mon file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

3. Run CAN communication script in the second terminal

```shell
make can-comm file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

4. Select `device_info_request` then `broadcast`
1. You should see output in the `can-mon` terminal

### Rebuilding Firmware Only Changes

As you are developing, in `ot3-firmware`, if you only make changes to the firmware you only need to rebuild the
firmware.

```shell
make local-rebuild-firmware file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

> Note: There is a quiet version of the command `local-rebuild-firmware-quiet`

### Rebuilding All Changes

As you are developing, if you need to rebuild all local containers run the following command.

```shell
make local-rebuild file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

> Note: There is a quiet version of the command `local-rebuild-quiet`