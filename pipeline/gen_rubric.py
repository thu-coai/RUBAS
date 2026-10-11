import argparse
import ast
import concurrent.futures
import json
import os

from openai import OpenAI

from utils import *

prompt_template = ""
tool_path = ""


def get_tools(data_instance):
    """
    Extract tool information from the data instance for prompt display.
    """
    return_envs = []
    envs = data_instance.get("environments", [])
    for env in envs:
        name = env.get("name", "")
        function = env.get("tools", [])
        with open(os.path.join(tool_path, f"{name}.json"), "r", encoding="utf-8") as f:
            all_tools = json.load(f)
        tool_lists = []
        for tool in all_tools:
            if tool.get("function", {}).get("name", "") in function:
                tool_lists.append(tool.get("function", {}))
        return_envs.append(
            {
                "name": name,
                "tools": tool_lists,
                "parameters": env.get("parameters", {}),
            }
        )

    return return_envs


def _extract_tool_code_from_python(env_name: str, tool_names):
    """
    Load the Python file for an environment and extract source code for the given tool functions.
    Only functions whose names appear in `tool_names` are returned.
    Handles both top-level functions and class methods.
    """
    if not tool_names:
        return ""

    py_path = os.path.join(tool_path, f"{env_name}.py")
    if not os.path.exists(py_path):
        return ""

    try:
        with open(py_path, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError:
        return ""

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""

    lines = source.splitlines(keepends=True)
    snippets = []
    
    def extract_function_code(func_node):
        """Extract source code for a function node."""
        start = func_node.lineno - 1  # Convert 1-indexed to 0-indexed
        end_lineno = getattr(func_node, "end_lineno", None)
        if end_lineno is None:
            # Fallback: estimate end by finding max lineno in function body
            end_lineno = func_node.lineno
            for child in ast.walk(func_node):
                if hasattr(child, "lineno") and child.lineno > end_lineno:
                    end_lineno = child.lineno
        # end_lineno is 1-indexed and inclusive, add 1 for exclusive slicing
        end = end_lineno + 1
        return "".join(lines[start:end])
    
    # Search for functions in the AST (handles both top-level and class methods)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in tool_names:
            snippets.append(extract_function_code(node))

    if not snippets:
        return ""

    result = [f"# Environment: {env_name}"]
    result.extend(snippets)
    return "\n\n".join(result)


def build_environment_and_tool_info(data_instance):
    """
    Build strings for:
    - ENVIRONMENT_INFORMATION: parameters used to initialize mock tool environments
    - TOOLS_RESPONSE_INFORMATION: Python implementations of the tools used in the environments

    Only functions whose names are listed in each environment's `tools` field are included.
    """
    envs = data_instance.get("environments", [])
    env_info_parts = []
    tool_code_parts = []

    for env in envs:
        name = env.get("name", "")
        parameters = env.get("parameters", {})
        if name:
            env_info_parts.append(
                f"Environment: {name}\nParameters: "
                f"{json.dumps(parameters, ensure_ascii=False)}"
            )

        tool_names = env.get("tools", []) or []
        if name and tool_names:
            code = _extract_tool_code_from_python(name, tool_names)
            if code:
                tool_code_parts.append(code)

    environment_information = "\n\n".join(env_info_parts)
    tools_response_information = "\n\n".join(tool_code_parts)    
    return environment_information, tools_response_information


def process_item(index, item):
    """Process a single item for rubric generation.
    Process a single item to generate the rubric.
    """
    # Check if rubric already exists
    # if "rubric" in item and item["rubric"] is not None:
    #     return index, item["rubric"]  # Already processed

    # Skip if prompt_type is None (not classified yet)
    if item["data_type"] is None:
        return index, None

    get_envs = get_tools(item)
    tools_json = ""
    for env in get_envs:
        tools_json += f"Environment: {env.get('name', '')}\n"
        tools_json += f"Tools: {json.dumps(env.get('tools', []), ensure_ascii=False)}\n"

    # Build optional environment and tool implementation info
    environment_information = ""
    tools_response_information = ""
    if item["data_type"] in ("Benign", "Sensitive", "Harmful"):
        (
            environment_information,
            tools_response_information,
        ) = build_environment_and_tool_info(item)
    if item["data_type"] == "Harmful":
        tools_response_information = "NA"

    notes_to_evaluator = item.get("notes_to_evaluator", "-")

    base_replacements = (
        prompt_template.replace("{{INSTRUCTION}}", item["instruction"])
        .replace("{{DATA_TYPE}}", str(item["data_type"]))
        .replace("{{TOOLS_JSON}}", tools_json)
        .replace("{{ENVIRONMENT_INFORMATION}}", environment_information)
        .replace("{{TOOLS_RESPONSE_INFORMATION}}", tools_response_information)
        .replace("{{NOTES_TO_EVALUATOR}}", notes_to_evaluator)
    )

    if item["data_type"] == "Benign":
        prompt = (
            base_replacements.replace("{{RISK_PATTERN}}", "NA for benign data")
            .replace("{{RISK_PATTERN_SUBTYPE}}", "NA for benign data")
            .replace("{{RISK_PATTERN_SUBTYPE_DES}}", "-")
        )
    else:
        prompt = (
            base_replacements.replace("{{RISK_PATTERN}}", str(item["risk_pattern"]))
            .replace("{{RISK_PATTERN_SUBTYPE}}", str(item["risk_pattern_subtype"]))
            .replace("{{RISK_PATTERN_SUBTYPE_DES}}", get_risk_pattern_subtype_description(item["risk_pattern_subtype_id"]))
        )
    # print(prompt)
    response = llm_api("", prompt)
    # response = None
    # print(response)
    if response is None:
        print(f"Failed to get response for item {index}")
        return index, None

    usage = extract_usage_stats(response)
    if usage is not None:
        print(usage["prompt_tokens"], usage["completion_tokens"])

    response_content = extract_response_content(response)
    if not isinstance(response_content, str):
        print(f"Failed to extract response content for item {index}")
        return index, None

    rubric = parse_json(response_content)
    if rubric is None:
        print(f"Failed to parse rubric for item {index}")
        return index, None

    return index, rubric



def gen_rubric(pipeline_config, data_path, workers, max_items):
    """
    Main function for generating rubrics.
    Read data, concurrently call LLM to generate rubrics, and then save the results.
    """
    with open(data_path,"r", encoding="utf-8") as f:
        data = json.load(f)

    with open("./template/rubric_template.txt","r", encoding="utf-8") as f1:
      gen_template = f1.read()

    global prompt_template
    prompt_template = gen_template  
    global tool_path
    tool_path = pipeline_config.tools_path

    # Collect items that need processing
    items_to_process = []
    for i, item in enumerate(data):
        # Only process if rubric doesn't exist/is None AND prompt_type is not None
        if ("rubric" not in item or item["rubric"] is None) and item["data_type"] is not None:
        # if ("rubric" not in item or item["rubric"] is None) or (item["rubric"]["response_safety"]["enabled"]==True and item["rubric"]["response_safety"]["forbidden_regex"]==[]):
            items_to_process.append((i, item))
            if max_items and len(items_to_process) >= max_items:
                break

    if not items_to_process:
        print("No items to process")
        return

    worker_count = max(1, int(workers or 1))
    print(f"Processing {len(items_to_process)} items with {worker_count} workers...")

    # Process items in parallel
    rubrics_to_update = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(process_item, index, item): index
            for index, item in items_to_process
        }

        # Collect results
        for future in concurrent.futures.as_completed(future_to_index):
            try:
                index, rubric = future.result()
                if rubric is not None:
                    rubrics_to_update[index] = rubric
                    print(f"Successfully processed item {index}")
                else:
                    print(f"Failed to process item {index}")
            except Exception as e:
                print(f"Error processing future: {e}")

    # Update data with new rubrics
    for index, rubric in rubrics_to_update.items():
        data[index]["rubric"] = rubric

    # Save to file with error handling for circular references
    try:
        with open(data_path,"w", encoding="utf-8") as w:
            json.dump(data, w, indent=4)
        print(f"Successfully saved {len(rubrics_to_update)} new rubrics to file")
    except (ValueError, TypeError) as e:
        print(f"Error saving to JSON: {e}")
        # Try to identify problematic items
        for i, item in enumerate(data):
            try:
                json.dumps(item)
            except (ValueError, TypeError):
                print(f"Problematic item at index {i}: {item.keys()}")
                break

