import os
import sys
import subprocess

builtin_commands = ("type", "echo", "exit", "pwd", "cd")


def path_exists(path: str) -> bool:
    if os.access(path, os.X_OK):
        return True
    return False


def in_path(command: str, paths: list[str]) -> tuple[str, bool]:
    for path in paths:
        fullpath = os.path.join(path, command)
        if path_exists(fullpath):
            return fullpath, True

    return "", False


def handle_commands(input: str, paths: list[str]):
    if input.startswith("echo"):
        args: str = input[5:]
        if not args.startswith("'"):
            # print(
            #     f"""yup I am inside that "'""  \n args: {args}  \n split: {args.split()}"""
            # )

            arg_list = []
            quote_count = 0
            for arg in args.split(" "):
                quote_count += arg.count('"')

                if quote_count % 2 == 0 and arg == "":
                    continue
                arg_list.append(arg)

            args = " ".join(arg_list)

        # Why are we replacing "'" with "" ?
        # It's because, if the user explicitly adds the "'" we need
        # to remove those in the final ouput becasue it doesn't look good
        print(args.replace('"', "").strip())
        # print(args, file=sys.stderr)
    elif input.startswith("pwd"):
        args: str = input[4:]
        print(os.getcwd())
    elif input.startswith("cd"):
        args: str = input[3:]
        homedir = os.getenv("HOME")
        dir = homedir if args == "~" and homedir else args

        if os.path.exists(dir):
            os.chdir(dir)
        else:
            print(f"cd: {args}: No such file or directory")
    elif input.startswith("type"):
        string_after = input[5:]

        if string_after in builtin_commands:
            print(f"{string_after} is a shell builtin")
        else:
            fullpath, path_exist = in_path(string_after, paths)

            if path_exist:
                print(f"{string_after} is {fullpath}")
            else:
                print(f"{string_after}: not found")


def main():
    paths = os.environ["PATH"].split(os.pathsep)

    while True:
        try:
            sys.stdout.write("$ ")
            user_inp = input()

            if user_inp.startswith(builtin_commands):
                if user_inp == "exit":
                    break

                handle_commands(user_inp, paths)
            elif user_inp.startswith("cat"):
                command = [s for arg in user_inp.split("'") if (s := arg.strip())]
                subprocess.run(command)
            else:
                command = user_inp.split(" ")
                fullpath, path_exist = in_path(command[0], paths)
                if not path_exist:
                    print(f"{user_inp}: command not found")
                else:
                    subprocess.run(command)

        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
