#!/usr/bin/python3
"""Our BaseModel that defines all common attributes/methods for other classes
"""
import uuid
from datetime import datetime
import models


class BaseModel():
    """The main class"""
    def __init__(self, *args, **kwargs):
        """Constructor of the instance. Uses kwargs if not empty"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, time)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return an user friendly representation
           of the isinstance
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Updates the public instance attribute
        updated_at with the current date and time"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing
        all the __dict__ keys / values of the instance"""
        my_dict = self.__dict__.copy()
        my_dict.update({"__class__": self.__class__.__name__})
        my_dict.update({"created_at": self.created_at.isoformat()})
        my_dict.update({"updated_at": self.updated_at.isoformat()})
        return (my_dict)
