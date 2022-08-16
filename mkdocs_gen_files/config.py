from mkdocs.config.config_options import File, OptionallyRequired


class ListOfItems(OptionallyRequired):
    def __init__(self, option_type, default=[], required=False):
        super().__init__(default, required)
        self.option_type = option_type
        self.option_type.warnings = self.warnings

    def pre_validation(self, config, key_name):
        self._config = config
        self._key_name = key_name

    def run_validation(self, value):
        result = []
        for item in value:
            self.option_type.pre_validation(self._config, self._key_name)
            result.append(self.option_type.validate(item))
            self.option_type.post_validation(self._config, self._key_name)
        return result


class ListOfFiles(ListOfItems):
    def __init__(self):
        super().__init__(File(exists=True))
