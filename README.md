# SiFli USB customer-allocated PID repository

[English](README_EN.md)

123 test

## 概览

这是SiFli VID（0x38F4）下客户分配PID的资源库。对于仅生产小批量产品的个人或公司而言，获取专属USB供应商ID（VID）成本较高。因此我们提供使用SiFli VID下分配的PID作为替代方案。
若您的设备搭载了带USB接口的SiFli芯片，且所申请的PID用于该接口，即可使用本服务。

## 你什么时候需要申请 PID？

若您的SF32使用自定义USB类且需主机端非标准驱动程序，则需定制PID。例如使用CherryUSB的自带例程，因其默认已采用预分配的特定类PID，故无需定制PID。

## VID 与 PID 基础

- **VID（Vendor ID）**：由 USB-IF 分配的 16 位厂商编号，用于识别 USB 设备制造商。SiFli 的 VID 为 **0x38F4**。
- **PID（Product ID）**：由 VID 持有人自行分配的 16 位编号，用于区分旗下具体产品。
- 当 USB 设备连接到主机时，`VID + PID` 组合可唯一识别该设备，并协助操作系统加载正确的驱动或固件。

## 可分配的 PID 范围

- SiFli 将 0x38F4 名下的 **0x9000 – 0xAFFF** 区段专门开放给基于 **SF32** 设计平台或其他获授权的 SiFli 项目。
- 如需申请其它区段的 PID，请先通过邮件沟通需求与理由。

## 申请流程

### 0. 申请前提条件

若未满足以下任一条件，请先完善项目后再提交 PR；在此之前的申请会被拒绝：

- 项目需包含公开可访问的源代码或设计文件仓库，并展示 USB 接口相关的固件、驱动或电路实现。
- 文档中应能找到 USB 设备所依赖的硬件原理图或软件代码，证明其确实基于 SF32 或其他获授权的 SiFli 方案。
- 仓库必须采用公认的开源软件或开源硬件许可证，并在源代码仓库根目录提供 `LICENSE` 文件。若项目同时含硬件与软件，两者都需具备对应的开源许可。

若项目暂未满足以上要求，请在条件完备后再申请。我们当前的 PID 资源充足，无需着急提交。

### 1. Fork 仓库

在 GitHub 上 Fork 本仓库至你的账号或组织，建议随后创建独立的功能分支，以便提交 PR。

### 2. 准备本地环境

克隆 Fork 后的仓库到本地，并安装 Python 3.11 及以上版本（用于运行辅助脚本）。确认根目录下存在 `pid/` 目录。

### 3. 分配 PID

使用随仓库提供的 CLI 脚本查看已注册的 PID 并分配新编号：

```bash
python3 pid_cli.py list
# 随机分配一个可用 PID，并根据提示填写 index.toml 字段
python3 pid_cli.py assign
# 若想手动指定 PID，可使用：
# python3 pid_cli.py assign --pid 0x9ABC
```

脚本会在 `pid/0xNNNN/` 目录下生成 `index.toml` 文件，并引导填写必须字段。

### 4. 完善资料

- 请根据项目实际情况补充 `index.toml` 的字段，示例结构见下文。
- 可在同目录下放置最多两张 PNG 图片（建议控制在 1 MB 内）展示产品、原理图或应用场景。

### 5. 提交 Pull Request

确认所有文件均已就绪后，提交到 Fork 仓库并创建 PR。请遵循仓库根目录 `.github/pull_request_template.md` 中的检查清单，确保说明项目如何使用 SiFli / SF32 技术，并附上验证方式。维护者审核通过后，PID 即正式生效。

## 目录结构示例

```
pid/
  └── 0x9001/
        ├── index.toml
        ├── board_front.png (可选)
        └── board_back.png  (可选)
```

## `index.toml` 字段要求

`index.toml` 必须使用 UTF-8 编码，并包含以下键值：

```toml
title = "示例项目名称"
desc = "约 120 字符内的中文或英文简介"
owner = "负责组织或团队名称"
license = "SPDX 格式的许可证标识，例如 MIT、Apache-2.0"
homepage = "https://example.com"
repository = "https://github.com/example/project"
```

- `title`：简洁明了的产品名称。
- `desc`：突出设备的用途或主要亮点。
- `owner`：维护或拥有该产品的公司、组织或个人团队。
- `license`：请使用 SPDX 标准标识，确保授权协议清晰。
- `homepage` / `repository`：需提供可靠的公开链接；如暂未上线，可填写 `""`。

## 图片规范

- 每个 PID 条目最多提交两张 PNG 图片，单个文件建议控制在 1 MB 以内。
- 文件名推荐使用 `snake_case`，例如 `board_front.png`。
- 图片内容应突出产品或相关示意图，避免泄露敏感信息。

## Pull Request 检查清单

- [ ] 所选 PID 未与现有条目冲突。
- [ ] `index.toml` 信息完整、格式正确。
- [ ] 附件图片（如有）符合数量与命名规范。
- [ ] PR 描述中说明项目与 OpenSiFli 技术（如 SF32）的关联。
- [ ] 提交记录与作者信息准确无误。

## 支持与反馈

如在 PID 分配、SF32 硬件或仓库流程方面遇到问题，请通过 Issue 与我们联系。
