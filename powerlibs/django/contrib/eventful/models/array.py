class ArrayEventfulModelMixin:
    def get_array_fields(self):
        for field in self._meta.fields:
            class_name = field.__class__.__name__
            if class_name in ('ArrayField',):
                yield field.name

    def serialize(self):
        serialized_data = super().serialize()
        for field_name in self.get_array_fields():
            if field_name in serialized_data:
                value = serialized_data[field_name]
                if isinstance(value, str):
                    if value.startswith('{') and value.endswith('}'):
                        serialized_data[field_name] = value[1:-1].split(',')
                    elif value.startswith('[') and value.endswith(']'):
                        serialized_data[field_name] = eval(value)

        return serialized_data
