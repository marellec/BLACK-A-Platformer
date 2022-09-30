
from base_folder import Folder, abstract_Folder_method
from base_labels import Label
from base_traits_entities import Entity


class EntityPack(metaclass=Folder):
    
    folder_name = "entities"
    folder_item_name = "entity"
    
    label: Label
    
    entities: dict[Label, Entity]
    
    def __init__(self, 
                 label: Label,
                 entities: tuple[Entity, ...]):
        self.label = label
        self.entities = {e.label : e for e in entities}

    def add_entity(self, entity: Entity):
        self.entities[entity.label] = entity
        return self
    
    @abstract_Folder_method
    def remove_entity(self, entity_label: Label):
        pass
    
    @abstract_Folder_method
    def __getitem__(self, entity_label: Label) -> Entity:
        pass