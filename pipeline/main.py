from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import os
from pathlib import Path
from gen_ins import *
from gen_rubric import *
from utils import *
from test_env_init import *


# Configure multiple targets here. Supported modes process them in order.
PROCESS_TARGETS = [
    {
        "data_type": "Sensitive",
        "gen_instance_data_path": "./rubric_eval_data/gpt5.1-5/sampled_sensitive.json",
    },
    {
        "data_type": "Benign",
        "gen_instance_data_path": "./rubric_eval_data/gpt5.1-5/sampled_benign.json",
    },
    {
        "data_type": "Harmful",
        "gen_instance_data_path": "./rubric_eval_data/gpt5.1-5/sampled_harmful.json",
    },
]


def get_process_targets():
    """
    Validate and normalize processing targets.
    """
    if not PROCESS_TARGETS:
        raise ValueError("PROCESS_TARGETS is empty. Please configure at least one target.")

    normalized_targets = []
    for target in PROCESS_TARGETS:
        if not isinstance(target, dict):
            raise TypeError(f"Each PROCESS_TARGETS item must be a dict, got {type(target).__name__}")

        target_data_type = target.get("data_type")
        target_data_path = target.get("gen_instance_data_path")
        if not target_data_type or not target_data_path:
            raise ValueError(
                "Each PROCESS_TARGETS item must contain 'data_type' and 'gen_instance_data_path'."
            )

        normalized_targets.append(
            {
                "data_type": target_data_type,
                "gen_instance_data_path": target_data_path,
            }
        )

    return normalized_targets


def print_current_target(target):
    print("\n" + "=" * 80)
    print(f"Processing data_type: {target['data_type']}")
    print(f"Target file: {target['gen_instance_data_path']}")
    print("=" * 80)


def run_data_generation(pipeline_config, data_type, gen_instance_data_path, workers, subtype_ids=None):
    """
    Run the data generation process.
    Generate instruction sets and append them to the existing data file.
    """
    instruction_set = gen_instruction_set(
        data_type=data_type,
        pipeline_config=pipeline_config,
        sample_n=1,
        tools_category_number=1,
        workers=workers,
        benign_sample_n=20,
        subtype_ids=subtype_ids,
    )
    if not instruction_set:
        print("No instruction set generated.")
        return

    print("Saving data to ", gen_instance_data_path)
    
    # Ensure data directory and file exist
    if not os.path.exists(gen_instance_data_path):
        os.makedirs(os.path.dirname(gen_instance_data_path), exist_ok=True)
        with open(gen_instance_data_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(gen_instance_data_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
    print("len of existing_data: ", len(existing_data))
    print("len of ins_set: ", len(instruction_set))
    print("len of final data: ", len(existing_data + instruction_set))
    instruction_set = existing_data + instruction_set
    with open(gen_instance_data_path, "w", encoding="utf-8") as w:
        json.dump(instruction_set, w, indent=4)


def run_rubric_generation(pipeline_config, gen_instance_data_path, workers, max_items):
    """
    Run the rubric generation process.
    """
    gen_rubric(pipeline_config, gen_instance_data_path, workers=workers, max_items=max_items)


def run_env_validation(pipeline_config, gen_instance_data_path):
    """
    Run the environment validation process.
    Validate if the environment configuration in the generated data is valid.
    """
    test_gen_data_environments_initialize_with_parameters(gen_instance_data_path, pipeline_config.tools_path)
    list_environment(gen_instance_data_path)
    print("Data env are valid")


def reformat_env_invalid_data(pipeline_config, gen_instance_data_path):
    """
    Reformat invalid data.
    Remove data items that cannot be initialized.
    """
    with open(gen_instance_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_data = []
    for item in data:
        if test_one_data_env_initialize_with_parameters(pipeline_config.tools_path, item):
            new_data.append(item)
    print(len(new_data))
    with open(gen_instance_data_path, "w", encoding="utf-8") as w:
        json.dump(new_data, w, indent=4)


def list_environment(gen_instance_data_path):
    environment = {}
    sub_type= {}
    with open(gen_instance_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        for env in item["environments"]:
            if env["name"] not in environment:
                environment[env["name"]] = 1
            else:
                environment[env["name"]] += 1
        if "risk_pattern_subtype" in item:
            if item["risk_pattern_subtype"] not in sub_type:
                sub_type[item["risk_pattern_subtype"]] = 1
            else:
                sub_type[item["risk_pattern_subtype"]] += 1
    sorted_sub_type = dict(sorted(sub_type.items(), key=lambda item: item[1], reverse=True))
    print(sorted_sub_type)
    print(len(sub_type))

    sorted_env = dict(sorted(environment.items(), key=lambda item: item[1], reverse=True))
    print(sorted_env)
    print(len(environment))


def execute_mode_for_target(mode, pipeline_config, target, workers, rubric_max_items, subtype_ids=None):
    """
    Execute the corresponding task for a single target.
    """
    data_type = target["data_type"]
    gen_instance_data_path = target["gen_instance_data_path"]

    if mode == 0:
        run_data_generation(pipeline_config, data_type, gen_instance_data_path, workers, subtype_ids)
    elif mode == 1:
        run_rubric_generation(pipeline_config, gen_instance_data_path, workers, rubric_max_items)
    elif mode == 2:
        run_env_validation(pipeline_config, gen_instance_data_path)
    elif mode == 3:
        reformat_env_invalid_data(pipeline_config, gen_instance_data_path)


def execute_mode(mode, pipeline_config, workers, rubric_max_items, subtype_ids=None):
    """
    Execute the corresponding task based on the specified mode.
    Supported modes iterate over PROCESS_TARGETS in order.
    """
    for target in get_process_targets():
        print_current_target(target)
        execute_mode_for_target(
            mode=mode,
            pipeline_config=pipeline_config,
            target=target,
            workers=workers,
            rubric_max_items=rubric_max_items,
            subtype_ids=subtype_ids,
        )

def main():
    """
    Main entry function.
    Parse command line arguments and configure pipeline settings.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help="Provide one mode (0: data, 1: rubric, 2: validate, 3: reformat invalid data)."
    )
    parser.add_argument("--workers", type=int, default=4, help="Worker count for rubric generation.")
    parser.add_argument("--rubric-max-items", type=int, default=50, help="Optional limit for rubric generation.")
    parser.add_argument("--subtype-ids", type=str, nargs="+", help="List of RiskPatternSubtype IDs to run (e.g., 1.1 2.1).")
    args = parser.parse_args()
    mode =args.mode

    # Get the directory where the current script is located
    current_dir = Path(__file__).resolve().parent
    # Build tools path: pipeline/../collected_tools/combined_tools
    tools_path = current_dir.parent / "collected_tools" / "combined_tools"
    
    if not tools_path.exists():
        print(f"Warning: Tools path does not exist: {tools_path}")
    
    pipeline_config = PipelineConfig(str(tools_path))

    execute_mode(mode, pipeline_config, args.workers, args.rubric_max_items, args.subtype_ids)


if __name__ == "__main__":
    main()
