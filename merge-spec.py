import yaml
import sys
from collections.abc import Mapping

def merge_yaml(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        yaml1 = yaml.safe_load(f1)
        yaml2 = yaml.safe_load(f2)

    merged = merge_dicts(yaml1, yaml2)

    with open(output_file, 'w') as outfile:
        yaml.dump(merged, outfile, default_flow_style=False)

def merge_dicts(dict1, dict2):
    """
    Recursively merge two dictionaries without simple overriding.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result:
            if isinstance(result[key], Mapping) and isinstance(value, Mapping):
                result[key] = merge_dicts(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                result[key] = merge_lists(result[key], value)
            else:
                # If types don't match or it's a simple value, keep the original
                pass
        else:
            result[key] = value
    return result

def merge_lists(list1, list2):
    """
    Merge two lists, attempting to match items by content.
    """
    merged = list1.copy()
    for item in list2:
        if item not in merged:
            merged.append(item)
    return merged

if __name__ == "__main__":
    
    file1, file2, output_file = './spec/openapi.yaml', './spec/customapi.yaml', './spec/merged.yaml'
    merge_yaml(file1, file2, output_file)
    print(f"Merged YAML written to {output_file}")