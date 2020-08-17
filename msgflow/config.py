from envyaml import EnvYAML


def load_yaml(path):
    """
    Args:
        path (str): File path of yaml configuration file

    Returns:
        Dict[str, Any]:
    """
    return EnvYAML(path, include_environment=False).export()
