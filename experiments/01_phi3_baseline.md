# Experiment 01: Phi-3 Baseline

## Objective

Test how Phi-3 Mini answers a factual question without additional information from an external source.

## Setup

- Model: Phi-3 Mini
- Runtime: Ollama
- Operating system: Windows
- Hardware: Intel Core i7-1355U, 32 GB RAM, no NVIDIA GPU
- Python: 3.11.9
- Prompt: "What is the purpose of RAG?"

## Experiment 1: Basic Prompt

### Prompt

> What is the purpose of RAG?

### Result

Phi-3 answered that RAG stands for "Resource Access Gateway" and described it as a networking and information-technology concept.

### Assessment

The answer was incorrect for this project. In the context of generative AI, RAG means Retrieval-Augmented Generation.

## Experiment 2: System Prompt

### System Prompt

> You are a helpful assistant. Answer questions accurately and concisely. If you are uncertain about an answer, say that you are uncertain rather than inventing information.

### User Prompt

> What is the purpose of RAG?

### Result

Phi-3 answered that RAG stands for "Robotics and Automation Group."

### Assessment

The system prompt changed the response but did not produce the correct definition. This suggests that prompting alone did not provide the model with the missing information.

## Observation

The base model can produce fluent but incorrect answers. The next stages of the project will investigate whether external information retrieval and fine-tuning can improve the system's responses.

## Next Experiment

Test whether providing Phi-3 with reliable source information improves its answer.
