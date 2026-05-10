import os


builtin_commands = ("type", "echo", "exit", "pwd", "cd", "jobs")

"""
Shell Operators

In Unix
    Std ouput is identified by 1 
    Std error is identified by 2
    
"""
redirect_operators = (">", "1>", "2>")
append_operators = (">>", "1>>", "2>>")


external_paths = os.environ["PATH"].split(os.pathsep)
