class JSONEventfulModelMixin:
    def get_json_fields(self):
        for field in self._meta.fields:
            class_name = field.__class__.__name__
            if class_name in ('HStoreField', 'JSONField'):
                yield field.name

    def serialize(self):
        serialized_data = super().serialize()

        for field_name in self.get_json_fields():
            value = serialized_data[field_name]
            if isinstance(value, str):
                serialized_data[field_name] = eval(value)

        return serialized_data
