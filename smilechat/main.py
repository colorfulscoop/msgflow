import logging
import os
from .config import load_yaml
from .content import INIT_CONFIG
from .content import INIT_APP
from .controller import Controller


def load_module(name):
    components = name.split(".")
    mod = __import__(".".join(components[:-1]), fromlist=[components[-1]])
    return getattr(mod, components[-1])


def load_class_and_config(yaml_dic, key):
    service_dict = yaml_dic[key]
    cls_name = service_dict["name"]
    config = service_dict.get("config", dict())
    return load_module(cls_name), config


def build_service(yaml_dic):
    cls, config = load_class_and_config(yaml_dic, "service")
    service = cls(config)
    return service


def build_post_service(yaml_dic, service):
    key = "post_service"
    if key in yaml_dic:
        cls, config = load_class_and_config(yaml_dic, "post_service")
        return cls(config)
    else:
        logging.info(
            '"post_service" is not defined in config file. '
            '"service" is used for "post_service" instead.'
        )
        return service


def build_app(yaml_dic, post_service):
    cls, config = load_class_and_config(yaml_dic, "app")
    service = cls(service=post_service, config=config)
    return service


class Main:
    def init(self, dir=".", config_file="config.yml", app_file="app.py"):
        config_path = os.path.join(dir, config_file)
        app_path = os.path.join(dir, app_file)
        with open(config_path, "w") as fd:
            fd.write(INIT_CONFIG)
        with open(app_path, "w") as fd:
            fd.write(INIT_APP)

    def run(self, config_file):
        # Set logging
        logging.basicConfig(level=logging.INFO)

        yaml_dic = load_yaml(config_file)
        service = build_service(yaml_dic)
        post_service = build_post_service(yaml_dic, service=service)
        app = build_app(yaml_dic=yaml_dic, post_service=post_service)
        controller = Controller(service, app)

        controller.start_handle()


if __name__ == "__main__":
    import fire

    fire.Fire(Main)
