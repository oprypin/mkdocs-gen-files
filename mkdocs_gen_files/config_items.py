from __future__ import annotations

from mkdocs.config.config_options import File, OptionallyRequired, ValidationError


class ListOfItems(OptionallyRequired):
    def __init__(self, option_type, default=[], required=False):
        super().__init__(default=None if required else default, required=required)
        self.option_type = option_type
        self.option_type.warnings = self.warnings

    def pre_validation(self, config, key_name):
        self._config = config
        self._key_name = key_name

    def run_validation(self, value):
        if not isinstance(value, list):
            raise ValidationError(f"Expected a list of items, but a {type(value)} was given.")

        result = []
        for item in value:
            self.option_type.pre_validation(self._config, self._key_name)
        for item in value:
            result.append(self.option_type.validate(item))
        for item in value:
            self.option_type.post_validation(self._config, self._key_name)
        return result


class ListOfFiles(ListOfItems):
    def __init__(self, required=False):
        super().__init__(File(exists=True), required=required)
