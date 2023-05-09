"""Location for OT-3 e2e pytest functions."""
import copy
from dataclasses import is_dataclass, fields
from typing import Callable, Dict, Any

import pytest

from tests.e2e.docker_interface.e2e_system import (
    DefaultContainers,
    E2EHostSystem,
    ExpectedBindMounts,
)
from tests.e2e.docker_interface.module_containers import ModuleContainers
from tests.e2e.docker_interface.ot3_containers import OT3SystemUnderTest
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.test_mappings import get_e2e_test_parameters
from tests.e2e.utilities.results.results import FinalResult


def __inner_convert_to_dict(obj):
    """Method to handle converting dataclass into raw values.

    Base logic pulled from source code of dataclasses.asdict.
    Added handling for set objects. Removed handling for named tuples
    """
    if is_dataclass(obj):
        result = []
        for field in fields(obj):
            value = __inner_convert_to_dict(getattr(obj, field.name))
            result.append((field.name, value))
        return dict(result)
    elif isinstance(obj, (list, tuple)):
        return type(obj)(__inner_convert_to_dict(v) for v in obj)
    elif isinstance(obj, set):
        return {frozenset((k, v) for k, v in __inner_convert_to_dict(instance).items()) for instance in obj}

    elif isinstance(obj, dict):
        return dict((__inner_convert_to_dict(k), __inner_convert_to_dict(v)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def convert_to_dict(obj) -> Dict[str, Any]:
    return __inner_convert_to_dict(obj)


@pytest.mark.parametrize("test_def", get_e2e_test_parameters())
def test_e2e(
    test_def: SystemTestDefinition,
    ot3_model_under_test: Callable[[str], OT3SystemUnderTest],
    modules_under_test: Callable[[str], ModuleContainers],
    local_mounts_under_test: Callable[[str], ExpectedBindMounts],
    default_containers_under_test: Callable[[str], DefaultContainers],
) -> None:
    """Runs e2e tests for OT-3.

    If there is a failure, will log custom test output to console.
    """
    e2e_system = E2EHostSystem(
        ot3_containers=ot3_model_under_test(test_def.yaml_config_relative_path),
        module_containers=modules_under_test(test_def.yaml_config_relative_path),
        expected_binds_mounts=local_mounts_under_test(
            test_def.yaml_config_relative_path
        ),
        default_containers=default_containers_under_test(
            test_def.yaml_config_relative_path
        ),
    )
    actual_results = convert_to_dict(FinalResult.get_actual_results(e2e_system).ot3_results)
    expected_results = convert_to_dict(FinalResult.get_expected_results(test_def).ot3_results)
    assert actual_results == expected_results
