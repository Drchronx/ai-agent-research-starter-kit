# 大模型调用法情感分析

## 适用任务

当用户要求调用大模型判断情感、希望使用自定义标签集合，或没有训练数据但有 API key 时使用本说明。

## 调用脚本

脚本：`scripts/llm_sentiment.py`

## 常用命令

```bash
python scripts/llm_sentiment.py --input "texts.csv" --text-column "text" --output "llm_sentiment.csv" --model "gpt-4.1-mini" --api-key-env OPENAI_API_KEY --labels "positive,negative,neutral"
```

OpenAI-compatible 服务：

```bash
python scripts/llm_sentiment.py --input "texts.csv" --text-column "text" --output "llm_sentiment.csv" --model "model-name" --base-url "https://api.example.com/v1" --api-key-env MODEL_API_KEY
```

## 参数

- `--api-key-env`：保存 API key 的环境变量名。
- `--base-url`：兼容 OpenAI SDK 的服务地址。
- `--labels`：允许输出的标签，逗号分隔。
- `--max-rows`：测试时限制行数。
- `--sleep`：请求间隔，避免限流。

## 输出

输出 CSV，新增模型返回的 `label`、`confidence`、`reason`。

## 边界

脚本只支持 OpenAI-compatible Chat Completions 接口。若用户要求其他 SDK，当前 skill 不支持。
