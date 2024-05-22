#!/usr/bin/python3
"""This is the file storage class for SITESWIFT"""
import json
import os


class FileStorage:
    """This class will manage storage of SITESWIFT instances"""
    __file_path = "file.json"
    __objects = {}


    def all(self, cls=None):
        """Returns the dictionary __objects"""
        
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        
        return self.__objects
    
    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        FileStorage.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(new_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as f:
                new_dict = json.load(f)
            for key, value in new_dict.items():
                FileStorage.__objects[key] = eval(value['__class__'])(**value)
                
    def delete(self, obj=None):
        """To delete an object from __object"""
        
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
                
    
    def get(self, cls, id):
        """To retrieve one object"""
        
        if cls is not None and id is not None:
            key = cls.__name__ + '.' + id
            if key in self.__objects:
                return self.__objects[key]
        return None
    
    
    def count(self, cls=None):
        """To count the number of objects in storage"""
        
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return len(new_dict)
        return len(self.__objects)  