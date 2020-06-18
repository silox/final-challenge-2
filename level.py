from constants import RESOLUTION
import object_classes as obj_cls


class Level:
    def __init__(self, level_id, background=None, music=None, objects=None, app=None):
        self._objects = {} if objects is None else Level.create_gui_objects(objects, app)
        self._num_of_objects = len(self._objects)
        self._app_instance = app
        self.level_id = level_id
        self.background = obj_cls.ImageObject((0, 0), background, RESOLUTION)
        self.music = music

    def handle_event(self, event):
        for gui_object in self.get_all_objects():
            if self._app_instance.enabled_input_objects and gui_object.obj_id not in self._app_instance.enabled_input_objects:
                continue
            if gui_object.reactive:
                gui_object.handle_event(event)

    def add_object(self, name, new_object):
        if name in self._objects:
            raise KeyError('Object name already exists')

        self._objects[name] = obj_cls.object_type_dict[new_object['type']](**new_object['options'])
        self._num_of_objects += 1

    def get_all_objects(self):
        yield from self._objects.values()

    def get_object(self, name):
        return self._objects[name]

    @staticmethod
    def create_gui_objects(objects, app=None):
        '''Transform every dictionary object definition into GUI object'''
        result_objects = {}
        for obj_id, (name, params) in enumerate(objects.items()):
            SpecificObject = obj_cls.object_type_dict[params['type']]
            result_objects[name] = SpecificObject(**params['options'], app=app, obj_id=obj_id, name=name)
        return result_objects
