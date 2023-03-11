import cmd
import sys
import re
from shlex import split
sys.path.append('C:/Users/kshed/OneDrive/Desktop/programming/AirBnB_clone')
from models.base_model import BaseModel
from models import storage


classes = ['BaseModel']

def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    square_bracket = re.search(r"\[(.*?)\]", arg)
    
    if curly_braces is None:
        if square_bracket is None:
            return [i.strip(",") for i in split(arg)]
        
        else:
            line = [i.strip(",") for i in split(arg[:square_bracket.span()[0]])]
            line.append(square_bracket.group())
            return(line)
    else:
        line = [i.strip(",") for i in split(arg[:curly_braces.span()[0]])]
        line.append(curly_braces.group())
        return(line)


    
 
def check_args(args):
    l = parse(args)
    if len(l) == 0:
        print ('** class name missing **')
        return False
    try:    
        if l[0] not in classes:
            print("** class doesnt exist **")
            return False
    except IndexError:
            pass
    return (l)

class HBNBCommand(cmd.Cmd):
    """console for the AIRBNB clone project

    Args:
        cmd (_type_): _description_
    """
    prompt = "(HBNB) "
    
    def default(self, line: str):
        action_map = {
            "create": self.do_create
        } 
        match = re.search(r"\.", line)
        
        if match:
            arg = [arg[:match.span()[0]],arg[:match.span()[1]]]
            match = re.search(r"\((.*?)\)", arg)
            if match:
                command = [arg[1][:match.span()[0]], match.group()[1:-1]]
                call = "{} {}".format(arg[0], command[1])
                return action_map[command[0]](call)
            
        print("*** Unknown syntax: {}".format(line))
        return False
    
    
    def do_create(self, line):
        
        args = parse(line)
        
        if args:
            print(eval(args[0])().id)
            storage.save()
    
    def do_show(self, line):
        arg = check_args(line)
        if arg:
            key = arg[1].join(arg[0])
            dicts = storage.all()
            for key, value in dicts.items():
                if key == "{}.{}".format(arg[0], arg[1]):
                    print(value)
                    return 
            print ("** instance id missing **")
                
    def do_destory(self,line):
        arg = check_args(line)
        if arg:
            key = arg[1].join(arg[0])
            dicts = storage.all()
            key = "{}.{}".format(arg[0], arg[1])
            if key in dicts.keys():
               del storage.all()[key]
               storage.save()
               return 
            print ("** instance id missing **")
            
    def do_all(self, line):
        arg = parse(line)
        rect = []
        if len(arg) == 0:
            for i in storage.all():
                rect.append(str(storage.all()[i]))
        
            print(rect)            
        
        else:
            key = arg[0]
            ret = []
            cls = "__class__"
            for keys in storage.all():
                splt = keys.split(".")
                if splt[0] == key:
                    ret.append(str(storage.all()[keys]))
                   
            
            if bool(ret) == False:
                print ("** class doesn't exist **")
            else:
                print(ret) 
                
    def do_update(self,line):
            arg = check_args(line)
            key = "{}.{}".format(arg[0], arg[1])
            obj = storage.all().get(key)
            obj._dict_[arg[2]] = arg[3]
            storage.save()
        
    
    def emptyline(self):
        """
            does nothing when an empty line is enterd
        """
        pass
        
    def do_quit(self, line):
        """
        DESCRIPTION:
            to exit out of the command line
        Args:
            doesn't take argumenet.
        Returns:
            BOL: True
        """
        return True
    
    def do_EOF(self, line):
        """
        DESCRIPTION:
            exits the console
        Args:
            doesn't take an argument.
        Returns:
            BOL: True
        """
        return True
    
    
    
    
    
if __name__ == "__main__":
    HBNBCommand().cmdloop()
