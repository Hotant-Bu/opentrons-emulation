#!/bin/bash

# Build all simulators in ot3-firmware
# Create a directory for each simulator to live
# On local-ot3-firwmare-builder container create a volume for each simulator and bind each simulator directory to it
# On each OT-3 Firmware emulator container attach its respective volume

echo "Building ot3-firmware"

(
  cd /ot3-firmware && \
  cmake --preset host-gcc10 && \
  cmake --build ./build-host -j $(expr $(nproc) - 1) && \
  cmake --build --preset tests --target state-manager-build
)

echo "Creating simulator directories"

mkdir -p \
  /volumes/pipettes_volume \
  /volumes/head_volume \
  /volumes/gantry_x_volume \
  /volumes/gantry_y_volume \
  /volumes/gantry_y_volume \
  /volumes/bootloader_volume \
  /volumes/gripper_volume \
  /volumes/state-manager-venv \
  /volumes/state-manager-dist

echo "Copying simulator files to simulator directories"

rm -f /volumes/pipettes-volume/pipettes-simulator
rm -f /volumes/head-volume/head-simulator
rm -f /volumes/gantry_x-volume/gantry-x-simulator
rm -f /volumes/gantry_y-volume/gantry-y-simulator
rm -f /volumes/bootloader-volume/bootloader-simulator
rm -f /volumes/gripper-volume/gripper-simulator
rm -rf /volumes/state-manager-venv/*
rm -rf /volumes/state-manager-dist/*

cp /ot3-firmware/build-host/pipettes/simulator/pipettes-single-simulator /volumes/pipettes-volume/pipettes-simulator
cp /ot3-firmware/build-host/head/simulator/head-simulator /volumes/head-volume/head-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /volumes/gantry-x-volume/gantry-x-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /volumes/gantry-y-volume/gantry-y-simulator
cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /volumes/bootloader-volume/bootloader-simulator
cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /volumes/gripper-volume/gripper-simulator
cp -r /ot3-firmware/build-host/.venv/* /volumes/state-manager-venv/
cp -r /ot3-firmware/state_manager/dist/* /volumes/state-manager-dist/
