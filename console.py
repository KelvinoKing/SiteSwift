#!/usr/bin/python3
"""This is the console for BookSwap"""
import cmd
import models
from models.base_model import BaseModel
from models.billing_cycle import BillingCycle
from models.hosting_plan import HostingPlan
from models.invoice import Invoice
from models.order import Order
from models.payment import Payment
from models.profile import Profile
from models.service import Service
from models.user import User
import shlex



class BookSwapCommand(cmd.Cmd):
    """"This is the console for BookSwap"""
    prompt = '(BookSwap) '
    classes = {
        'User': User,
        'Profile': Profile,
        'Service': Service,
        'HostingPlan': HostingPlan,
        'BillingCycle': BillingCycle,
        'Order': Order,
        'Invoice': Invoice,
        'Payment': Payment,
        }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True
    
    def emptyline(self):
        """Handles empty line"""
        pass

    def do_help(self, arg):
        """Prints help"""
        cmd.Cmd.do_help(self, arg)
        
    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict


    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in self.classes:
            new_dict = self._key_value_parser(args[1:])
            new_instance = eval(args[0])(**new_dict)
        else:
            print("*** class does not exist ***")
            return False
        
        print(new_instance.id)
        new_instance.save()


    def do_all(self, arg):
        """Prints all string representation of all instances"""
        if len(arg) == 0:
            print([str(v) for k, v in models.storage.all().items()])
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in models.storage.all().items() if arg in k])


    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **")

            
    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in models.storage.all():
                del models.storage.all()[key]
                models.storage.save()
            else:
                print("** no instance found **")


    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in models.storage.all():
                if len(args) == 2:
                    print("** attribute name missing **")
                elif len(args) == 3:
                    print("** value missing **")
                else:
                    try:
                        value = eval(args[3])
                    except (NameError, SyntaxError):
                        value = args[3]
                    setattr(models.storage.all()[key], args[2], value)
                    models.storage.save()
            else:
                print("** no instance found **")
                

    def do_count(self, arg):
        """Handles the '<class name>.count()' command"""
        args = arg.split()
        if len(args) != 1:
            print("** class name missing **")
        else:
            class_name = args[0]
            if class_name in self.classes:
                instances = [str(v) for k, v in models.storage.all().items() if args[0] in k]
                print(len(instances))
            else:
                print("** class doesn't exist **")
                

    def default(self, line):
        """Called on an input line when the command prefix is not recognized"""
        if '.' in line:
            try:
                line_parts = line.split('.')
                class_name = line_parts[0]
                command_with_args = line_parts[1]
                command_parts = command_with_args.split('(')
                command = command_parts[0]
                args = command_parts[1].rstrip(')').split(',')
                if command == 'all':
                    self.do_all(class_name)
                elif command == 'count':
                    self.do_count(class_name)
                elif command == 'show':
                    self.do_show(class_name + ' ' + args[0])
                elif command == 'destroy':
                    self.do_destroy(class_name + ' ' + args[0])
                elif command == 'update':
                    self.do_update(class_name + ' ' + args[0] + ' ' + args[1] + ' ' + args[2])
            except Exception as e:
                print("*** Unknown syntax: " + line)
        else:
            print("*** Unknown syntax: " + line)


if __name__ == '__main__':
    BookSwapCommand().cmdloop()