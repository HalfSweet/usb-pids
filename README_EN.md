# SiFli USB Customer-Allocated PID Repository

[中文版](README.md)

## Overview

This repository documents how SiFli allocates USB Product IDs (PIDs) under the USB-IF Vendor ID (VID) **0x38F4** for customer projects. Obtaining a dedicated VID can be expensive for individuals or teams building low-volume devices. We therefore offer PID assignments under our VID for devices that integrate SiFli chips with USB interfaces.

## When Should You Request a PID?

Request a PID if your SF32-based product implements a custom USB class that requires host-side drivers beyond standard class implementations. For example, if you use CherryUSB sample firmware that already includes predefined class PIDs, you usually do not need a custom PID.

## VID & PID Basics

- **VID (Vendor ID)**: 16-bit identifier assigned by the USB-IF to identify the manufacturer. SiFli’s VID is **0x38F4**.
- **PID (Product ID)**: 16-bit identifier assigned by the VID holder to distinguish individual products.
- When connected, the combination `VID + PID` uniquely identifies the USB device and helps the host load the appropriate driver or firmware.

## Available PID Range

- SiFli reserves **0x9000 – 0xAFFF** under VID 0x38F4 for projects based on **SF32** designs or other authorized SiFli solutions.
- If you need a PID outside this range, contact us to discuss the use case first.

## Application Workflow

### 0. Prerequisites

Before submitting a pull request, make sure your project meets all of these requirements; otherwise the request will be rejected:

- A publicly accessible repository or documentation that includes the USB-related firmware, drivers, or circuit design.
- Evidence (schematics, source code, or documentation) showing that the device is built on SF32 or another approved SiFli platform.
- Open-source licensing under a recognized software or hardware license, with a `LICENSE` file in the repository root. If the project spans both hardware and software, both parts must be licensed appropriately.

If you do not yet meet these criteria, please wait until you do. We have ample PID capacity, so there is no rush.

### 1. Fork the Repository

Fork this repository on GitHub and create a feature branch in your fork for the PID request.

### 2. Prepare Your Local Environment

Clone your fork locally. Install Python 3.11 or later (required for the helper CLI) and ensure the repository root contains the `pid/` directory.

### 3. Allocate a PID

Use the provided CLI script to review existing entries and allocate a new PID:

```bash
python3 pid_cli.py list
# Assign a random available PID and follow the prompts
python3 pid_cli.py assign
# To specify a PID manually:
# python3 pid_cli.py assign --pid 0x9ABC
```

The script creates a directory `pid/0xNNNN/`, scaffolds `index.toml`, and guides you through the required fields.

### 4. Complete Project Details

- Fill in all fields in `index.toml` according to your project details (see specification below).
- Optionally add up to two PNG images in the same directory to showcase the product or diagrams (recommendation: keep each under 1 MB).

### 5. Open a Pull Request

Once everything is ready, commit the changes to your fork and open a PR. Follow the bilingual checklist in `.github/pull_request_template.md`, explaining how your project leverages SiFli / SF32 technology and how you validated the submission. Maintainers will review and merge approved requests.

## Directory Structure Example

```
pid/
  └── 0x9001/
        ├── index.toml
        ├── board_front.png (optional)
        └── board_back.png  (optional)
```

## `index.toml` Specification

Each project entry must include an `index.toml` file encoded in UTF-8 with the following keys:

```toml
title = "Example Project Name"
desc = "Short summary within ~120 characters"
owner = "Responsible organization or team"
license = "SPDX license identifier, e.g. MIT, Apache-2.0"
homepage = "https://example.com"
repository = "https://github.com/example/project"
```

- `title`: concise product name.
- `desc`: highlight the device purpose or signature features.
- `owner`: organization or team managing the product.
- `license`: SPDX-compliant identifier to ensure license clarity.
- `homepage` / `repository`: stable public URLs; use empty string `""` if not available.

## Image Guidelines

- Up to two PNG files per PID entry, each ideally below 1 MB.
- Use `snake_case` filenames such as `board_front.png`.
- Choose images that showcase the product or relevant diagrams while avoiding confidential content.

## Pull Request Checklist

- [ ] Selected PID is unused within the `pid/` directory.
- [ ] `index.toml` is complete and correctly formatted.
- [ ] Optional PNG assets comply with guidelines.
- [ ] PR description explains how the project uses SiFli / SF32 technology.
- [ ] Commit authorship is accurate.

## Support

If you have questions regarding PID allocation, SF32 hardware, or repository processes, please open an issue or contact us via <usb-pid@opensifli.com>.
