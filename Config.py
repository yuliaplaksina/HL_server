import json


class Config(object):
    __conf = {}

    @staticmethod
    def set(path: str):
        config = Config()
        config.read(path)
        config.__complete()

        return config

    @property
    def address(self):
        return self.__conf['address']

    @property
    def port(self):
        return self.__conf['port']

    @property
    def cpu_limit(self):
        return self.__conf['cpu-limit']

    @property
    def document_root(self):
        return self.__conf['document_root']

    def read(self, path: str):
        with open(path, 'r') as config_file:
            self.__conf = json.load(config_file)

    def __complete(self):
        self.set_default('address', '0.0.0.0')
        self.set_default('port', 80)
        self.set_default('cpu-limit', 2)
        self.set_default('document_root', 'test')

    def set_default(self, key: str, default):
        if key not in self.__conf:
            self.__conf[key] = default
