import tempfile
import os
from msgflow.config import load_yaml


def write(fp, content):
    fp.write(content)
    fp.flush()


def test_load_yaml():
    yaml_str = """
service:
  name: msgflow.service.CliService
  config:
    user_name: you
    """
    want = {
        "service": {
            "name": "msgflow.service.CliService",
            "config": {"user_name": "you"},
        }
    }
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        write(fp, yaml_str)

        # Load and test config
        got = load_yaml(fp.name)
        assert got == want


def test_load_yaml_parse_with_env_var():
    yaml_str = """
service:
  name: msgflow.service.CliService
  config:
    user_name: ${USER_NAME}
    password: ${PASSWORD}
    """

    # Set environment variable
    os.environ["USER_NAME"] = "name_from_env"
    os.environ["PASSWORD"] = "password_from_env"

    want = {
        "service": {
            "name": "msgflow.service.CliService",
            "config": {"user_name": "name_from_env", "password": "password_from_env"},
        }
    }
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        write(fp, yaml_str)

        # Load and test config
        got = load_yaml(fp.name)
        assert got == want

    # Remove environment varialbe
    del os.environ["USER_NAME"]
    del os.environ["PASSWORD"]


def test_load_yaml_parse_with_env_var_but_not_defined():
    yaml_str = """
service:
  name: msgflow.service.CliService
  config:
    user_name: ${USER_NAME}
    password: ${PASSWORD}
    """

    # Set environment variable
    os.environ["USER_NAME"] = "name_from_env"
    # Not define PASSWORD env var
    # os.environ["PASSWORD"] = "password_from_env"

    want = {
        "service": {
            "name": "msgflow.service.CliService",
            "config": {"user_name": "name_from_env", "password": "${PASSWORD}"},
        }
    }
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        write(fp, yaml_str)

        # Load and test config
        got = load_yaml(fp.name)
        assert got == want

    # Remove environment variable
    del os.environ["USER_NAME"]
