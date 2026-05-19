---
name: big-data-labeling-variable-construction
description: Route text-labeling requests across LDA topic modeling, sklearn baselines, pretrained transformer models, and OpenAI-compatible LLM labeling. First inspect the dataset and infer columns/defaults automatically, then wait for explicit user confirmation before execution.
---

# Big Data Labeling Workflow

Use this skill from `F:\Python\课程\OpenClaw\cnki\skills\big-data-labeling-variable-construction`.

## Mandatory interaction pattern

1. First recommend one technical route.
2. After the user uploads or points to the dataset, inspect the first 10 rows automatically.
3. Infer what you can by yourself:
   - text column
   - label column
   - document id column
   - default train/test split
   - default epoch
   - default batch size
4. Show the inferred plan back to the user.
5. Do not run any actual labeling, training, or API calls yet.
6. Only after the user explicitly replies with `确认无误，请执行`, run the chosen script.

## What the user usually does not need to provide

These should be inferred or defaulted whenever possible:

- 文本列名
- 标签列名
- 文档ID列名
- epoch
- batch size
- 训练集/测试集比例

## What the user still needs to provide when the skill cannot infer it

- `LDA主题建模`
  - usually only the dataset path
- `sklearn常见机器学习方法`
  - usually only the dataset path
- `预训练模型`
  - dataset path
  - model name
- `调用大语言模型标注数据`
  - dataset path
  - label set
  - `base_url`
  - `api_key`
  - model name

## Recommended flow

### Step 1: Recommend a route

```powershell
python scripts/labeling_workflow.py --task-description "我有中文文本，已有标签，想先做一个轻量分类基线" --label-status labeled --output-dir reports/labeling-workflow-demo
```

### Step 2: Prepare a confirmation plan from the dataset

```powershell
python scripts/prepare_labeling_plan.py assets/sample_labeled_text_dataset.csv --category sklearn --output-dir reports/labeling-plan-demo
```

This script should be used before real execution. It inspects the first 10 rows, infers likely columns, fills default parameters, and writes `labeling_plan.json`.

### Step 3: Wait for user confirmation

You must wait for this exact confirmation before execution:

`确认无误，请执行`

### Step 4: Run the actual method script

## Pretrained-model environment check

Before running `BERT/ERNIE`, first check whether `torch` and `transformers` are installed:

```powershell
python scripts/check_pretrained_env.py
```

If dependencies are missing, guide the user to the official PyTorch pages instead of hardcoding one install command:

- PyTorch 官网: [https://pytorch.org/](https://pytorch.org/)
- 官方安装页: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

Recommended interaction:

1. Tell the user whether `torch` / `transformers` are installed.
2. If missing, ask the user to install them from the official PyTorch install page.
3. If the machine has NVIDIA GPU, remind the user to choose the matching CUDA build.
4. Ask the user to reply `依赖已安装` before retrying the pretrained route.

## Script list

### 1. LDA主题建模

```powershell
python scripts/lda_topic_model.py assets/sample_topic_corpus.csv --text-col text --id-col doc_id --topic-range 2-10 --output-dir reports/lda-demo
```

### 2. sklearn常见机器学习方法

```powershell
python scripts/sklearn_svm_labeling.py assets/sample_labeled_text_dataset.csv --text-col text --label-col label --output-dir reports/sklearn-svm-demo
python scripts/sklearn_knn_labeling.py assets/sample_labeled_text_dataset.csv --text-col text --label-col label --output-dir reports/sklearn-knn-demo
python scripts/sklearn_random_forest_labeling.py assets/sample_labeled_text_dataset.csv --text-col text --label-col label --output-dir reports/sklearn-rf-demo
python scripts/sklearn_sgd_labeling.py assets/sample_labeled_text_dataset.csv --text-col text --label-col label --output-dir reports/sklearn-sgd-demo
```

### 3. 预训练模型

```powershell
python scripts/bert_labeling.py assets/sample_labeled_text_dataset.csv --text-col text --label-col label --model-name bert-base-chinese --output-dir reports/bert-demo
python scripts/ernie_labeling.py assets/sample_labeled_text_dataset.csv --text-col text --label-col label --model-name nghuyong/ernie-3.0-base-zh --output-dir reports/ernie-demo
```

### 4. 调用大语言模型标注数据

```powershell
python scripts/openai_llm_labeling.py assets/sample_text_dataset.csv --text-col text --labels 创新,风险,政策 --base-url https://api.openai.com/v1 --api-key YOUR_KEY --model gpt-4.1-mini --output-dir reports/openai-labeling-demo
```

## Install dependencies

```powershell
python -m pip install -r scripts/requirements.txt
```
