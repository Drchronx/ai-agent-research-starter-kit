# GitHub 发布安全检查报告

检查日期：2026-05-19

## 结论

已生成面向 GitHub 发布的清洁版目录：`GitHub发布清洁版`。本清洁版未包含原始第三方课程目录、压缩包、安装包和超过阈值的大文件；未发现明确可用的真实 API Key、GitHub Token、AWS Key 或 Bearer Token。

## 已执行处理

- 仅复制以下四个目录：
  - `教学资料`
  - `零基础教学包`
  - `综合学术部署包`
  - `本地Skills功能分类库`
- 排除 `.zip/.rar/.7z/.exe/.msi/.pyc/.log/.tmp/.bak/.ttf/.otf` 等不适合公开仓库的文件。
- 排除 `__pycache__`、`.ipynb_checkpoints`、`node_modules`、`.cache` 等缓存目录。
- 排除所有真实 `config.json`，并生成或保留 `config.example.json`。
- 将本地路径和用户名替换为占位写法，例如 `<本项目路径>`、`C:\Users\<用户名>`。
- 将 API Key 示例替换为占位写法，例如 `<你的OPENROUTER_API_KEY>`。
- 清理 Office 文档内部 XML 中的本地路径和文档作者元数据。

## 生成统计

- 复制文件数：3253
- 清洗文本文件数：62
- 清洗 Office 文件数：21
- 排除文件数：9
- 排除目录数：9
- 排除 `config.json` 数：6
- 生成 `config.example.json` 数：6
- 生成错误：0

详细机器记录见 `release_build_stats.json`。

## 仍需人工确认

- 本清洁版保留了教学课件、手册、Skills 和案例材料。公开前仍需确认这些内容是否全部属于你可公开分享的范围。
- 文档中保留了 AMiner、AI4Scholar、飞书、MCP 等平台名称和接入说明；这些不是密钥，但会暴露课程使用的平台路线。
- 如果后续新增真实数据、学生作业、会议纪要、文献 PDF、问卷原始数据、EEG 原始数据或机构材料，需要再次做脱敏检查。
- 如果仓库设为 public，建议启用 GitHub secret scanning，并避免提交任何 `.env`、`config.json`、账号截图和 API 控制台截图。

## 不建议上传的原始目录

以下原始目录未放入清洁版，不建议直接公开上传：

- `cc课程资料`
- `openclaw课件资料`
- `openclawssci特训营`
- `Python大语言模型与智能体前沿实证特训营`
- `Claude code工程科研`
- 根目录压缩包和安装包
