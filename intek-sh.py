#!/usr/bin/env python3
from os import environ, chdir, getcwd, path
import sys
import subprocess


def call_subprocess(command, args):
    """
    Call subprocess from external binaries
    @param:  command: command name
    @param:  args: command's arguments
    """
    if "./" in command:
        try:
            subprocess.call([command] + args)
        except FileNotFoundError:
            print("intek-sh: " + command + "No such file or directory")
        except PermissionError:
            print("intek-sh: " + command + ": Permission denied")
    elif 'PATH' in environ.keys():
        sub_paths = environ["PATH"].split(":")
        isFound = False
        for sub_path in sub_paths:
            command_path = sub_path + "/" + command
            if path.exists(command_path):
                isFound = True
                subprocess.call([command_path] + args)
                break
        if not isFound:
            print("intek-sh: " + command + ": command not found")
    else:
        print("intek-sh: " + command + ": command not found")


def call_cd(args):
    """
    Call cd built_in function
    @param: args: arguments of cd funtion
    """
    if not args or "$HOME" in args[0]:
        if "HOME" in environ.keys():
            home_dir = environ["HOME"]
            chdir(home_dir)
        else:
            print("intek-sh: cd: HOME not set")
    else:
        path_location = args[0]
        if path.isdir(path_location):
            chdir(path_location)
        else:
            print("intek-sh: cd: " + path_location +
                  ": No such file or directory")


def call_printenv(args):
    """
    Call printenv built_in function
    @param: args: arguments of printenv funtion
    """
    if not args:
        for key, value in environ.items():
            print(key + '=' + value)
    else:
        for arg in args:
            if arg in environ.keys():
                print(environ[arg])


def call_export(args):
    """
    Call export built_in function
    @param: args: arguments of export funtion
    """
    if not args:
        for key, value in environ.items():
            print("declare -x " + key + '=' + value)
    else:
        for arg in args:
            if "=" in arg:
                key = arg.split("=")[0]
                value = arg.split("=")[1]
                environ[key] = value
            else:
                environ[arg] = ""


def call_unset(args):
    """
    Call unset built_in function
    @param: args: arguments of unset funtion
    """
    for arg in args:
        if arg in environ.keys():
            environ.pop(arg)


def call_exit(args):
    """
    Call exit built_in function
    @param: args: arguments of exit funtion
    """
    if args:
        if len(args) > 1:
            print("intek-sh: exit: too many arguments")
        else:
            try:
                print("exit")
                sys.exit(int(args[0]))
            except ValueError:
                print('intek-sh: exit: ', end='')
                sys.exit(args[0])
    else:
        print("exit")
        sys.exit()


def call_function(command, args):
    """
    Call built_in function
    @param:  command: command name
    @param:  args: command's arguments
    """
    call_command = {"cd": call_cd,
                    "printenv": call_printenv,
                    "export": call_export,
                    "unset": call_unset,
                    "exit": call_exit
                    }
    call_command[command](args)


def main():
    """
    This is main function
    """
    # Mark flag to run while loop
    isLoop = True
    # Keep looping until there is any error occur
    while isLoop:
        # Try and except if there is end of file error
        try:
            # Take a list of input arguments
            list_input = input("intek-sh$ ").split()
            # If there is no input arguments -> loop until there is input arg
            while not list_input:
                list_input = input("intek-sh$ ").split()
            # The first argument is command name
            command = list_input[0]
            # The left arguments are command's arguments
            args = list_input[1:]
            # built_in functions in this program
            built_in = ["cd", "printenv", "export", "unset", "exit"]
            # Check if command is built_in function or external function
            # If command is external function, call subprocess
            if command not in built_in:
                call_subprocess(command, args)
            # If command is built_in function, call built_in function
            else:
                call_function(command, args)
        except EOFError:
            isLoop = False


if __name__ == '__main__':
    main()
