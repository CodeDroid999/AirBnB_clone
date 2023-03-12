#!/usr/bin/python3
"""This module contain the HBNB console"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import models
import json


class HBNBCommand(cmd.Cmd):
    """Command line interpreter HBNB"""
    prompt = "(hbnb) "
    class_list = ["BaseModel", "User", "Place", "State\
", "City", "Amenity", "Review"]

    def do_quit(self, args):
        """Quit command to exit the console"""
        return True

    def do_EOF(self, args):
        """EOF command to exit the console"""
        return True

    def emptyline(self):
        """Perform nothing when there's no commmand passed to the console"""
        pass

 

    def default(self, args):
        """default method that perfom actions when no command it's given"""
        count = 0
        if len(args.split(".")) > 1:
            class_name = args.split(".")[0]
            if class_name in HBNBCommand.class_list:
                try:
                    if args.split(".")[1] == "all()":
                        self.do_all(class_name)
                    if args.split(".")[1] == "count()":
                        for key, obj in storage.all().items():
                            if key.split(".")[0] == class_name:
                                count += 1
                        print(count)
                    if args.split(".")[1].split("(")[0] == "show":
                        id_ = args.split("\"")[1].split("\"")[0]
                        self.do_show(class_name + " " + id_)
                    if args.split(".")[1].split("(")[0] == "destroy":
                        id_ = args.split("\"")[1].split("\"")[0]
                        self.do_destroy(class_name + " " + id_)
                    if args.split(".")[1].split("(")[0] == "update":
                        arg_list = args.split(".", 1)[1]
                        arg_list = arg_list.split("(")[1][:-1].split(",")
                        if "{" not in arg_list[1]:
                            id_ = arg_list[0][1:-1]
                            name = arg_list[1][2:-1]
                            value = arg_list[2][1:]
                            if value[0] == "\"":
                                value = value[1:-1]
                            self.do_update(class_name + "\
 " + id_ + " " + name + " " + value)
                        else:
                            id_ = arg_list[0][1:-1]
                            arg_dict = args.split(".")[1]
                            arg_dict = arg_dict.split("(")[1][:-1]
                            arg_dict = arg_dict.split("{")[1]
                            arg_dict = "{" + arg_dict
                            dictionary = eval(arg_dict)
                            for key, value in dictionary.items():
                                ret = self.do_update(class_name + "\
 " + id_ + " " + key + " " + str(value))
                                if ret == -1:
                                    break
                except Exception:
                    cmd.Cmd.default(self, args)
        else:
            cmd.Cmd.default(self, args)


if __name__ == "__main__":
    comand = HBNBCommand()
    comand.cmdloop()
