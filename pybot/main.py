import yaml
from pybot.controller import Controller


def load_module(name):
    components = name.split('.')
    mod = __import__(".".join(components[:-1]), fromlist=[components[-1]])
    return getattr(mod, components[-1])


def build_object(yaml_dic, typ):
    service_dict = yaml_dic[typ]
    cls_name = service_dict["name"]
    config = service_dict.get("config", dict())
    service = load_module(cls_name)(config)
    return service


def main(config_file):
    yaml_dic = yaml.safe_load(open(config_file))

    service = build_object(yaml_dic, typ="service")
    app = build_object(yaml_dic, typ="app")
    controller = Controller(service, app)

    controller.start_handle()


if __name__ == "__main__":
    import fire

    fire.Fire(main)
