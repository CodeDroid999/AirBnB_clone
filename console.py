#!/usr/bin/python3
'''Command Line Interpreter'''
import cmd
import json
import re
import sys

from models import *
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_EOF(self, *args):
        '''Usage: EOF
           Function: Exits the program
        '''
        print()
        return True

    def do_quit(self, *args):
        '''Usage: quit
           Function: Exits the program
        '''
        # quit()
        return True

    def do_create(self, line):
        '''Usage: 1. create <class name> | 2. <class name>.create()
Function: Creates an instance of the class
        '''
        if line != "" or line is not None:
            if line not in storage.classes():
                print("** class doesn't exist **")
            else:
                # create an instance of the given class
                obj_intance = storage.classes()[line]()
                obj_intance.save()
                print(obj_intance.id)
        else:
            print("** class name missing **")

    def do_show(self, line):
        '''Usage: 1. show <class name> <id> | 2. <class name>.show(<id>)
Function: Shows the instance details of the class
        '''
        # check if class name and instance id was provided
        if line == "" or line is None:
            print("** class name missing **")

        else:
            # get all the arguments passed via the command line
            class_info = line.split(" ")
            if len(class_info) < 2:
                print("** instance id missing **")
            else:
                class_name = class_info[0]
                instance_id = class_info[1]
                # check if class name exists
                if class_name in storage.classes():
                    # check if instance_id exists
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        print(instance_dict)

                else:
                    print("** class doesn't exist **")

    def do_destroy(self, line):
        '''Usage: 1. destroy <class name> <id> | 2. <class name>.delete(<id>)
Function: Deletes the instance  of the class
        '''
        # check if class name and instance id was provided
        if line == "" or line is None:
            print("** class name missing **")

        else:
            # get all the arguments passed via the command line
            class_info = line.split(" ")
            if len(class_info) < 2:
                print("** instance id missing **")
            else:
                class_name = class_info[0]
                instance_id = class_info[1]
                # check if class name exists
                if class_name in storage.classes():
                    # check if instance_id exists
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        # delete this instance and save to json
                        del storage.all()[key]
                        storage.save()
                        return

                else:
                    print("** class doesn't exist **")

    def do_all(self, line):
        '''Usage: 1. all | 2. all <class name> | 3. <class name>.all()
Function: Prints the string representation of all instances
        '''
        instance_obj = storage.all()
        instance_list = []

        if line == "" or line is None:
            for key, value in storage.all().items():
                instance_list.append(str(value))
            print(instance_list)

        else:
            if line not in storage.classes():
                print("** class doesn't exist **")
                return
            else:
                for key, value in storage.all().items():
                    class_name, instance_id = key.split(".")
                    if line == class_name:
                        instance_list.append(str(value))
                print(instance_list)

    def do_update(self, line):
        '''Usage: 1. update <class name> <id> <attribute> <value> | \
2. <class name>.update(<id> <attribute> <value>) \
3. update <clas name> <id> <dictionary> \
4. <class name>.update(<id> <dictionary>) \
Function: Updates the instance of the class
        '''
        checks = re.search(r"^(\w+)\s([\S]+?)\s({.+?})$", line)
        if checks:
            # it is a dictionary
            class_name = checks.group(1)
            instance_id = checks.group(2)
            update_dict = checks.group(3)

            if class_name is None:
                print("** class name missing **")
            elif instance_id is None:
                print("** instance id missing **")
            elif update_dict is None:
                print("** attribute name missing **")
            else:
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        update_dict = json.loads(update_dict)

                        attributes = storage.attributes()[class_name]
                        # print(attributes)
                        for key, value in update_dict.items():
                            if key in attributes:
                                # print(key)
                                value = attributes[key](value)
                                # print(attributes[key])
                                setattr(instance_dict, key, value)
                                storage.save()

        else:
            # it isn't a dictionary
            checks = re.search(
                r"^(\w+)\s([\S]+?)\s\"(.+?)\"\,\s\"(.+?)\"", line)
            class_name = checks.group(1)
            instance_id = checks.group(2)
            attribute = checks.group(3)
            value = checks.group(4)

            if class_name is None:
                print("** class name missing **")
            elif instance_id is None:
                print("** instance id missing **")
            elif attribute is None:
                print("** attribute name missing **")
            elif value is None:
                print("** value missing **")
            else:
                #  check if class exists
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        # print(instance_dict)
                        attributes_dict = storage.attributes()[class_name]
                        # update attributes in the instance dictionary
                        # print(attributes_dict[attribute])
                        value = attributes_dict[attribute](
                            value)  # type casting
                        # print(attribute, value)
                        setattr(instance_dict, attribute, value)
                        storage.save()

    def emptyline(self):
        pass

    def precmd(self, line):
        # make the app work non-interactively
        if not sys.stdin.isatty():
            print()

        checks = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if checks:
            class_name = checks.group(1)
            command = checks.group(2)
            args = checks.group(3)

            if args is None:
                line = f"{command} {class_name}"
                return ''
            else:
                # print(args)
                args_checks = re.search(r"^\"([^\"]*)\"(?:, (.*))?$", args)
                # print(args_checks.group(1), args_checks.group(2))
                instance_id = args_checks[1]

                if args_checks.group(2) is None:
                    line = f"{command} {class_name} {instance_id}"
                else:
                    attribute_part = args_checks.group(2)
                    # print(attribute_part)
                    line = f"{command} {class_name} {instance_id} \
{attribute_part}"
                return ''

        return cmd.Cmd.precmd(self, line)
        # return ''

    def do_count(self, line):
        '''Usage: 1. count <class name> | 2. <class name>.count()
Function: Counts all the instances  of the class
        '''
        count = 0
        for key in storage.all().keys():
            class_name, instance_id = key.split(".")
            if line == class_name:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
