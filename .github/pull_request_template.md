## 描述 / Summary

请简要说明此次 PR 的目的与主要改动。  
Briefly describe the goal of this pull request and key changes.

## 提交类型 / Type

- [ ] PID 申请 / New PID entry
- [ ] 文档更新 / Documentation update
- [ ] 工具改进 / Tooling change
- [ ] 其他 / Other

## PID 变更检查清单 / PID Entry Checklist

（如本次 PR 与 PID 申请无关，可跳过此部分。）  
Skip if this PR does not add or modify PID entries.

- [ ] 所选 PID 在 `0x9000-0xAFFF` 范围内，且未被 `pid/` 目录现有条目占用。  
      Chosen PID is within 0x9000-0xAFFF and unused in `pid/`.
- [ ] 已新增 `pid/<PID>/index.toml`，字段完整且格式正确。  
      Added `pid/<PID>/index.toml` with all required fields.
- [ ] （可选）附上最多两张 PNG 图片，展示产品或相关示意图。  
      Added up to two optional PNG images highlighting the project.
- [ ] PR 描述中说明项目如何使用 OpenSiFli / SF32 技术。  
      PR description notes how the project leverages OpenSiFli / SF32 technology.

## 测试 / Verification

说明你是如何验证改动的，例如运行脚本、lint、手动检查等。  
Describe how you validated the changes (scripts, lint, manual verification, etc.).

## 其他备注 / Additional Notes

如有需要维护者关注的补充信息，请在此说明。  
Include any extra context reviewers should know.
