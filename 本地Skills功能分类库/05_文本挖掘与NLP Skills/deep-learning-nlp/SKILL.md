---
name: deep-learning-nlp
description: Paddle-based deep learning workflows from the course materials, including DNN/RNN text-style baselines and the CNN/LeNet image classification case using folder-labeled digit images. Use when a user asks Codex to train, evaluate, save, load, or predict with course DNN, CNN/LeNet, or RNN/GRU examples.
---

# Deep Learning NLP

## Operating Rule

Use this skill as a fixed command-line workflow. Do not write custom Paddle training code unless the user explicitly asks for a new model architecture outside this skill.

1. Decide whether the request is DNN, CNN/LeNet image classification, or RNN text-style modeling.
2. If unsupported, state that this skill cannot solve it and name the missing model or task type.
3. If supported, write a plan first. Include the model type, reference file, script, required data paths, training parameters, model output directory, and prediction output path when relevant.
4. Ask for missing columns, image folders, model directory, or output path.
5. Execute the referenced script with command-line arguments.

## Capability Map

- DNN text classification: read `references/dnn.md`, then call `scripts/paddle_text_classifier.py --model-type dnn`.
- CNN/LeNet image classification: read `references/cnn.md`, then call `scripts/paddle_image_cnn.py`.
- RNN/GRU text classification: read `references/rnn.md`, then call `scripts/paddle_text_classifier.py --model-type rnn`.

## Input Expectations

- DNN/RNN text training input: `.csv` or `.xlsx` with a text column and label column.
- CNN training input: image folders such as `data/CNN/train/0`, `data/CNN/train/1`, where folder names are labels.
- CNN prediction input: one image file or a folder of labeled/unlabeled images.

## Course Context

This skill follows the deep learning course notebooks:

- DNN and CNN concepts with Paddle.
- RNN/GRU concepts, training loop, evaluation, and save/load workflow.

The scripts adapt these course patterns to command-line workflows, so downstream AI only selects parameters and calls the CLI.
