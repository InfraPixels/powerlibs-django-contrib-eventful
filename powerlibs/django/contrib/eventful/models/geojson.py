import shapely.geometry
import shapely.wkt


class GeoJSONEventfulModelMixin:
    def get_geometry_fields(self):
        for field in self._meta.fields:
            class_name = field.__class__.__name__
            if class_name in ('PointField', 'LineStringField', 'PolygonField'):
                yield field.name

    def serialize(self):  # pragma: no cover
        serialized_data = super().serialize()

        for geometry_field_name in self.get_geometry_fields():
            new_field_name = geometry_field_name + '__geojson'
            value = serialized_data.get(geometry_field_name, None)

            if value is None:
                serialized_data[new_field_name] = value
                continue

            feature_str = value
            if ';' in feature_str:
                _, feature_str = value.split(';')
            feature = shapely.wkt.loads(feature_str)
            serialized_data[new_field_name] = shapely.geometry.mapping(feature)

        return serialized_data
