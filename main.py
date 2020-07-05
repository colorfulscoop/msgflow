import yaml
from controller import Controller


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def build_object(yaml_dic, typ):
    service_dict = yaml_dic[typ]
    cls_name = service_dict["name"]
    config = service_dict.get("config", dict())
    service = my_import(cls_name)(config)
    return service


def main(config_file):
    yaml_dic = yaml.load(open(config_file))

    service = build_object(yaml_dic, typ="service")
    app = build_object(yaml_dic, typ="app")
    controller = Controller(service, app)

    controller.start_handle()


if __name__ == "__main__":
    import fire

    fire.Fire(main)
