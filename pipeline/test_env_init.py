import importlib.util
import json
import sys
from pathlib import Path
import os


def _load_gen_data_instances(gen_data_path):
    with open(gen_data_path,"r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise AssertionError("Expected gen_data.json to contain a list of data instances.")
    return data


def _load_environment_class(env_name: str, tools_path):
    module_path = f"{tools_path}/{env_name}.py"
    assert os.path.exists(module_path), f"Environment module not found for {env_name}: {module_path}"

    spec = importlib.util.spec_from_file_location(env_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, f"Unable to load module spec for {env_name}"
    spec.loader.exec_module(module)

    assert hasattr(module, env_name), f"Module {module_path} is missing class {env_name}"
    return getattr(module, env_name)

def test_one_data_env_initialize_with_parameters(tools_path, instance):
    TOOLS_PATH = tools_path
    if str(TOOLS_PATH) not in sys.path:
        sys.path.insert(0, str(TOOLS_PATH))
    
    try:
        environments = instance.get("environments", [])
        assert environments, f"Instance does not define any environments."

        for env_index, env_config in enumerate(environments):
            env_name = env_config["name"]
            env_class = _load_environment_class(env_name, tools_path)

            try:
                env_instance = env_class(parameters=env_config.get("parameters"))
            except Exception as exc:  # pragma: no cover - explicit assertion path
                raise AssertionError(
                    f"Failed to initialize {env_name} "
                    f"for instance , environment {env_index}: {exc}"
                ) from exc

            if "parameters" in env_config:
                assert env_instance.parameters == env_config["parameters"], (
                    f"{env_name} did not retain provided parameters for "
                    f"instance , environment {env_index}"
                )

            requested_tools = set(env_config.get("tools", []))
            if requested_tools:
                available_tools = set(getattr(env_instance, "tool_list", []))
                missing_tools = requested_tools - available_tools
                assert not missing_tools, (
                    f"{env_name} is missing expected tools {sorted(missing_tools)} for "
                    f"instance , environment {env_index}"
                )
    except Exception as exc:
        return False

    return True



def test_gen_data_environments_initialize_with_parameters(gen_data_path, tools_path):
    GEN_DATA_PATH = gen_data_path
    TOOLS_PATH = tools_path
    if str(TOOLS_PATH) not in sys.path:
        sys.path.insert(0, str(TOOLS_PATH))
    instances = _load_gen_data_instances(GEN_DATA_PATH)
    assert instances, "gen_data.json must contain at least one instruction instance."

    for instance_index, instance in enumerate(instances):
        environments = instance.get("environments", [])
        assert environments, f"Instance {instance_index} does not define any environments."
    
        for env_index, env_config in enumerate(environments):
            env_name = env_config["name"]
            env_class = _load_environment_class(env_name, tools_path)

            try:
                env_instance = env_class(parameters=env_config.get("parameters"))
            except Exception as exc:  # pragma: no cover - explicit assertion path
                raise AssertionError(
                    f"Failed to initialize {env_name} "
                    f"for instance {instance_index}, environment {env_index}: {exc}"
                ) from exc

            if "parameters" in env_config:
                assert env_instance.parameters == env_config["parameters"], (
                    f"{env_name} did not retain provided parameters for "
                    f"instance {instance_index}, environment {env_index}"
                )

            requested_tools = set(env_config.get("tools", []))
            if requested_tools:
                available_tools = set(getattr(env_instance, "tool_list", []))
                missing_tools = requested_tools - available_tools
                assert not missing_tools, (
                    f"{env_name} is missing expected tools {sorted(missing_tools)} for "
                    f"instance {instance_index}, environment {env_index} {env_name}"
                )
