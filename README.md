# RUBAS: Rubric-Based Reinforcement Learning for Agent Safety

[**Paper**](https://arxiv.org/abs/2606.04051) · [**Training data**](data/train.json) · [**Data creation pipeline**](pipeline/) · [**Tool environments**](collected_tools/combined_tools/)

Official repository for **[RUBAS: Rubric-Based Reinforcement Learning for Agent Safety](https://arxiv.org/abs/2606.04051)** . Accepted to **Findings of EMNLP 2026**. A rubric-based reinforcement learning framework for improving the safety of tool-using language model agents. RUBAS evaluates agent behavior along four dimensions: **tool-use safety**, **argument safety**, **response safety**, and **helpfulness**, providing structured signals for safe and useful tool execution.

## Release scope

Stage 1 releases the **training data**, **data creation pipeline**, and **82 simulated environments with 811 tools**.

## Repository structure

```text
.
├── README.md
├── data/
│   └── train.json             # Released training data
├── pipeline/
│   ├── main.py                # Pipeline entry point
│   ├── gen_ins.py             # Instruction and environment generation
│   ├── gen_rubric.py          # Task-specific rubric generation
│   ├── test_env_init.py       # Environment initialization checks
│   ├── proc_data.py           # Dataset statistics utilities
│   ├── utils.py               # LLM client, tool loading, and risk taxonomy
│   ├── template/              # Instruction and rubric prompt templates
│   ├── README.md              # Pipeline usage
│   └── Rubric_README.md        # Rubric design notes
└── collected_tools/
    ├── README.md              # Tool inventory and source attribution
    └── combined_tools/
        ├── BaseEnv.py         # Shared tool interface
        ├── <Environment>.py   # Simulated environment implementation
        └── <Environment>.json # Tool schemas and metadata
```

## Training data

The released training file is a JSON array. Each record pairs a user instruction with the tools and initial environment state available to the agent, plus a rubric describing expected behavior.

| Split | Harmful | Sensitive | Benign | Total |
| --- | ---: | ---: | ---: | ---: |
| [Training](data/train.json) | 2,000 | 235 | 118 | 2,353 |

- **Harmful:** scenarios requiring refusal or stopping unsafe execution once a risk is recognized.
- **Sensitive:** tasks requiring useful tool execution while respecting safety constraints.
- **Benign:** low-risk tasks intended to preserve normal tool-use capabilities and task completion.

## Data creation pipeline

See the [pipeline guide](pipeline/README.md) for setup, LLM API configuration, and the full data creation workflow: instruction and environment generation (mode `0`), rubric generation (mode `1`), environment validation (mode `2`), and filtering (mode `3`).

## Tool environments

The release includes **82 simulated environments with 811 tool definitions**, covering areas such as communication, finance, healthcare, file management, travel, and infrastructure. Each environment pairs a Python implementation with a JSON tool schema. Simulated tools operate on mock data and local state.

### Sources and acknowledgments

The tool collection draws on **AgentSafetyBench**, **AgentAlign**, **SafeToolBench**, and **InjectAgent**. The checked-in tool metadata records each tool's source:

| Source | Tool definitions |
| --- | ---: |
| AgentSafetyBench | 571 |
| AgentAlign | 86 |
| SafeToolBench | 42 |
| InjectAgent | 112 |
| **Total** | **811** |

## Citation

If you use RUBAS or these resources in your research, please cite our paper:

```bibtex
@misc{loye2026rubas,
  title = {RUBAS: Rubric-Based Reinforcement Learning for Agent Safety},
  author = {Xian Qi Loye and Qinglin Su and Zhexin Zhang and Shiyao Cui and Qi Zhu and Fei Mi and Hongning Wang and Minlie Huang},
  year = {2026},
  eprint = {2606.04051},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG},
  url = {https://arxiv.org/abs/2606.04051}
}
```
