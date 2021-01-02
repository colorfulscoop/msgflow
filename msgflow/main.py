import os
from .config import load_yaml
from .content import INIT_CONFIG
from .content import INIT_APP
from .bot import Bot
from .protocol import Service
from .protocol import App
from .logging import print_json_log
import logging

logger = logging.getLogger(__file__)


def load_module(name: str):
    components = name.split(".")
    mod = __import__(".".join(components[:-1]), fromlist=[components[-1]])
    return getattr(mod, components[-1])


def load_class_and_config(yaml_dic: dict[str, str], key: str):
    service_dict = yaml_dic[key]
    cls_name = service_dict["name"]
    config = service_dict.get("config", dict())
    return load_module(cls_name), config


def build_service(yaml_dic: dict[str, str]) -> Service:
    cls, config = load_class_and_config(yaml_dic, "service")
    service = cls.from_config(config)
    return service


def build_post_service(yaml_dic: dict[str, str], service: Service) -> Service:
    key = "post_service"
    if key in yaml_dic:
        cls, config = load_class_and_config(yaml_dic, "post_service")
        return cls.from_config(config)
    else:
        print_json_log(
            logger,
            "debug",
            "`post_service` is not defined in config file. "
            "`service` is used for `post_service` instead.",
        )

        return service


def build_app(yaml_dic: dict[str, str]) -> App:
    cls, config = load_class_and_config(yaml_dic, "app")
    app = cls.from_config(config=config)
    return app


class Main:
    def init(self, dir=".", config_file="config.yml", app_file="app.py"):
        config_path = os.path.join(dir, config_file)
        app_path = os.path.join(dir, app_file)
        with open(config_path, "w") as fd:
            fd.write(INIT_CONFIG)
        with open(app_path, "w") as fd:
            fd.write(INIT_APP)

    def run(self, config_file: str, verbose: bool = False):
        # Set logging
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

        # Load config file
        yaml_dic = load_yaml(config_file)

        # Build service
        service: Service = build_service(yaml_dic)
        post_service: Service = build_post_service(yaml_dic, service=service)

        print_json_log(
            logger,
            "info",
            {
                "service": service.__class__.__name__,
                "post_service": post_service.__class__.__name__,
            },
        )

        # Build app
        app: App = build_app(yaml_dic=yaml_dic)

        # Build controller and start
        bot = Bot(service=service, post_service=post_service, app=app)
        bot.start()


if __name__ == "__main__":
    import fire

    fire.Fire(Main)
