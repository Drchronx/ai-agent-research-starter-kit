# AMiner MCP 接入说明

来源文档：

```text
https://zhipu-ai.feishu.cn/wiki/VHAGwiboFivCztkqknSciiQjn4d
```

AMiner MCP 服务地址：

```text
https://mcp.aminer.cn/sse
```

## 适合做什么

AMiner 更适合做学术知识图谱类任务：

- 查学者。
- 查机构。
- 看代表论文。
- 看专利和应用产出。
- 找某个方向的专家。
- 分析合作网络和学术影响。
- 和 OpenAlex、CNKI、AI4Scholar 交叉核验文献。

## 新手部署步骤

1. 获取 AMiner MCP Token。
2. 在你的 AI 客户端或 MCP 网关里添加 MCP server。
3. 重启客户端或 gateway。
4. 让 Agent 列出 AMiner 工具。
5. 用一个已知学者做测试。

配置模式：

```json
{
  "aminer": {
    "url": "https://mcp.aminer.cn/sse",
    "headers": {
      "Authorization": "Bearer ${AMINER_MCP_TOKEN}"
    }
  }
}
```

## 安全要求

- 不要把 Token 写进手册、论文、公开文档或聊天记录。
- 用 `${AMINER_MCP_TOKEN}` 作为占位符。
- 真实 Token 只放在本机私有配置或环境变量里。

## 推荐提示词

```text
请使用 AMiner MCP 查询[学者姓名]在[机构]的学术信息。
输出研究方向、代表论文、合作网络、专利或应用产出。
请区分 AMiner 返回的信息、你自己的推断和需要人工核验的信息。
```

```text
请使用 AMiner MCP 寻找“AI Agent 与科研创造力”方向的潜在专家。
输出学者、机构、代表作、可能相关性、可合作价值和需要核验的条目。
```

