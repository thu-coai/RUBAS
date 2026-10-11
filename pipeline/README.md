# Data creation pipeline

This pipeline creates tool-use safety tasks by pairing instructions with simulated environment states and task-specific rubrics. [`main.py`](main.py) runs one mode at a time and processes every configured target in order.

## Setup

Use Python 3.10 or newer. Reading the released dataset and running the included simulated environments use the Python standard library. The generation pipeline additionally imports `openai` and `tqdm`.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install openai tqdm
```

Data generation requires access to an LLM API. Before running modes `0` or `1`, configure `llm_api()` in [`utils.py`](utils.py). The checked-in function uses a placeholder API key and defaults to `gpt-5.1`.

For credentials, replace the placeholder assignment with an environment lookup:

```python
api_key = os.environ["OPENAI_API_KEY"]
```

Then set `OPENAI_API_KEY` in your shell. Review the model and request settings in the same function, and set the client's `base_url` if using another compatible endpoint. Setting the environment variable alone does not override the checked-in placeholder.

Modes `2` and `3` do not call the LLM API, but the pipeline entry point still imports the generation dependencies.

## Workflow and outputs

```text
Risk taxonomy + tool environments + prompt templates
                         ↓
Mode 0: Generate instructions and initial environment states
                         ↓
JSON records with instruction, environments, and task metadata
                         ↓
Mode 1: Generate task-specific rubrics
                         ↓
The same records with a rubric field added
                         ↓
Mode 2: Validate environments and print distributions
                         ↓
Mode 3: Filter out records that fail environment checks
                         ↓
The target JSON file contains only retained records
```

Each command runs only its selected mode; it does not automatically run the other steps. Validation can also be run immediately after mode `0`, and filtering can be followed by another validation run.

| Mode | What it produces | File behavior | LLM API required |
| --- | --- | --- | --- |
| `0` | Instruction–environment records with task and risk metadata. | Creates missing target files; appends to existing records. | Yes |
| `1` | A `rubric` for each successfully processed eligible record. | Updates the same target files in place. | Yes |
| `2` | Console validation results and environment/subtype counts. | Reads target files; creates no dataset or report file. | No |
| `3` | A filtered dataset containing records that pass environment checks. | Overwrites each target file with retained records. | No |

## 1. Configure targets

Edit `PROCESS_TARGETS` in [`main.py`](main.py). Each target specifies a task type and a JSON file:

```python
PROCESS_TARGETS = [
    {"data_type": "Harmful", "gen_instance_data_path": "./data/generated/harmful.json"},
    {"data_type": "Sensitive", "gen_instance_data_path": "./data/generated/sensitive.json"},
    {"data_type": "Benign", "gen_instance_data_path": "./data/generated/benign.json"},
]
```

All configured targets are processed in order, regardless of the selected mode. `data_type` selects the generation category in mode `0`; the other modes read records from the target file. Modes `1` through `3` require existing target files containing JSON arrays.

Run commands from `pipeline/` because prompt templates and relative target paths are resolved from the working directory. In the example above, `./data/generated/harmful.json` means `pipeline/data/generated/harmful.json`.

The checked-in targets point to `./rubric_eval_data/gpt5.1-5/`. The released training data is at [`../data/train.json`](../data/train.json). Use separate output files when creating new data.

Tool schemas and Python implementations are loaded from [`../collected_tools/combined_tools/`](../collected_tools/combined_tools/), with the directory resolved from the location of `main.py`.

## 2. Generate instructions and environment states — mode 0

From the repository root:

```bash
cd pipeline
python main.py --mode 0 --workers 4
```

The process in [`gen_ins.py`](gen_ins.py):

1. Selects risk-pattern subtypes and samples a risk category for harmful and sensitive tasks. Benign tasks use a separate generation branch.
2. Samples tool environments, weighting categories according to risk-related or benign keywords.
3. Builds a prompt from the instruction templates and sampled environment Python code.
4. Calls the LLM to generate an instruction, exposed tool names, initial environment parameters, and evaluator notes.
5. Parses successful responses, attaches task metadata, and appends the records to the target JSON array.

The current settings in `run_data_generation()` attempt one record per selected risk-pattern subtype for each harmful or sensitive target, and 20 records per benign target, using one sampled tool category per attempt. These settings are configured in code, not exposed as CLI flags. Failed generation attempts can reduce the output count.

The output includes `data_type`, `instruction`, and `environments`, plus generated fields such as `notes_to_evaluator`. Harmful and sensitive records also include risk-category, pattern, subtype, and subtype-ID metadata. Mode `0` does not generate rubrics or validate the generated environments.

To restrict harmful and sensitive generation to selected subtype IDs:

```bash
python main.py --mode 0 --workers 4 --subtype-ids 1.1 2.1
```

`--subtype-ids` does not restrict the benign generation branch. Repeating mode `0` appends more records; it does not replace or deduplicate existing records.

## 3. Generate rubrics — mode 1

```bash
python main.py --mode 1 --workers 4 --rubric-max-items 50
```

The process in [`gen_rubric.py`](gen_rubric.py):

1. Reads each target JSON array and selects records with a missing or `null` rubric and a non-null `data_type`.
2. Loads schemas for the tools listed in each record's environments.
3. Builds a rubric prompt using the instruction, task type, environment state, evaluator notes, and risk metadata where applicable. Tool implementation code is included for benign and sensitive tasks; harmful tasks use `NA` for that prompt section.
4. Calls the LLM and parses its JSON response.
5. Adds successful responses as the records' `rubric` fields and saves the target file.

Rubrics describe tool-use safety, argument safety, response safety, helpfulness, and reward weights. Existing non-null rubrics are skipped. Records whose rubric generation fails remain without a generated rubric and can be retried.

`--rubric-max-items` defaults to 50 eligible records **per target per run**. Use `0` to process all eligible records:

```bash
python main.py --mode 1 --workers 4 --rubric-max-items 0
```

See the [rubric design notes](Rubric_README.md) and [rubric template](template/rubric_template.json) for details.

## 4. Validate environments — mode 2

```bash
python main.py --mode 2
```

The checks in [`test_env_init.py`](test_env_init.py) read each record and:

1. Require at least one environment.
2. Load the Python module and class matching each environment's `name`.
3. Initialize the class with the record's `parameters`.
4. Check that supplied parameters are retained.
5. Check that the requested tool names appear in the environment's declared tool list.

If all records in a target pass, the pipeline prints environment and risk-pattern subtype distributions and a validation message. A failed assertion stops validation; this mode does not remove records or save a report.

These checks verify initialization and declared tool availability. They do not execute task trajectories or establish task solvability, tool behavior, or rubric correctness.

## 5. Filter invalid environments — mode 3

```bash
python main.py --mode 3
```

This mode applies the per-record environment checks described above, retains records that pass, prints the retained count, and overwrites the target JSON array. It does not repair failed records or create a separate rejected-record file. Keep a copy of the original file if you need to inspect discarded records.

After filtering, run mode `2` again to inspect the retained dataset's environment and subtype distributions.

## Command-line reference

```bash
python main.py --mode <MODE> [--workers N] [--rubric-max-items K] [--subtype-ids ID ...]
```

| Option | Default | Applies to | Purpose |
| --- | --- | --- | --- |
| `--mode` | `0` | All runs | Select one mode: `0`, `1`, `2`, or `3`. |
| `--workers` | `4` | Modes `0`, `1` | Number of concurrent generation workers. |
| `--rubric-max-items` | `50` | Mode `1` | Maximum eligible records per target; `0` removes the limit. |
| `--subtype-ids` | All subtypes | Mode `0`, harmful/sensitive targets | Restrict generation to the listed risk-pattern subtype IDs. |

Generation uses sampling and LLM responses, so rerunning the pipeline can produce different records. The CLI processes configured target files; it does not automatically merge generated files into the released `data/train.json`.
