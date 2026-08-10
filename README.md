# Shell From Scratch

An educational Unix-like shell written in Python, featuring a custom tokenizer, built-in commands, pipelines, redirection, background jobs, history, variables, and tab completion.

I built this project while working through the [CodeCrafters “Build Your Own Shell” challenge](https://codecrafters.io/challenges/shell). The goal was to look beneath the familiar command-line interface and learn how a shell parses input, locates executables, starts processes, connects pipes, and maintains interactive state.

> [!NOTE]
> This is a learning project rather than a POSIX-complete or production-ready shell.

## Features

- Interactive read-evaluate-execute loop with a `$ ` prompt
- External executable discovery through `PATH`
- Process creation using Python's `subprocess` module
- Hand-written state-machine tokenizer supporting:
  - single and double quotes
  - backslash escaping
  - malformed quote detection
- Multi-command pipelines using OS pipes
- Output redirection with `>`, `1>`, and `2>`
- Append redirection with `>>`, `1>>`, and `2>>`
- Background command execution and job tracking
- In-memory command history with optional `HISTFILE` persistence
- Shell-local variable declaration and expansion
- Readline/libedit tab completion for commands, files, and directories
- Programmable, command-specific completion through external scripts

## Quick Start

### Prerequisites

- A Unix-like environment such as macOS or Linux
- [Python](https://www.python.org/) 3.13 (the repository pins 3.13.2)
- [uv](https://docs.astral.sh/uv/)

`uv` can download the pinned Python version automatically if it is not already installed.

### Run locally

```sh
git clone https://github.com/vaibhav135/shell-from-scratch.git
cd shell-from-scratch
./your_program.sh
```

The launcher uses `uv` to run the `app.main` module with the repository configured on `PYTHONPATH`.

You can leave the shell by entering `exit` or pressing <kbd>Ctrl</kbd>+<kbd>C</kbd>.

## Example Session

```console
$ ./your_program.sh
$ echo "hello from my shell"
hello from my shell
$ type echo
echo is a shell builtin
$ type python3
python3 is /usr/bin/python3
$ pwd
/path/to/shell-from-scratch
$ echo hello | cat
hello
$ sleep 5 &
[1] 12345
$ jobs
[1]+  Running                 sleep 5 &
$ exit
```

Executable paths, process IDs, spacing, and working directories will vary by system.

## Built-in Commands

| Command | Description |
| --- | --- |
| `echo [arguments]` | Print tokenized arguments and expand declared variables |
| `type NAME` | Report whether a command is built in or resolve it through `PATH` |
| `pwd` | Print the current working directory |
| `cd PATH` | Change the shell's working directory; `cd ~` uses `HOME` |
| `exit` | Persist new history when configured, then exit the shell |
| `jobs` | Display tracked background jobs and their current state |
| `history [N]` | Show all history entries or the most recent `N` entries |
| `history -r FILE` | Read history entries from a file |
| `history -w FILE` | Save the current history by appending it to a file |
| `history -a FILE` | Append new history entries to a file |
| `declare NAME=VALUE` | Create a shell-local variable |
| `declare -p NAME` | Print a declared variable |
| `complete -C FILE COMMAND` | Register an external completion program for a command |
| `complete -p COMMAND` | Print a command's completion specification |
| `complete -r COMMAND` | Remove a command's completion specification |

### Variables

Variables created with `declare` are local to this shell implementation and can be expanded with `$NAME` or `${NAME}`:

```console
$ declare PROJECT=shell-from-scratch
$ echo $PROJECT
shell-from-scratch
$ declare -p PROJECT
declare -- PROJECT="shell-from-scratch"
```

Set `HISTFILE` before launching the program to load history at startup and append new entries when exiting normally. The history file must already exist:

```sh
export HISTFILE="$HOME/.shell_from_scratch_history"
touch "$HISTFILE"
./your_program.sh
```

## How It Works

The shell is organized into focused modules instead of placing the entire implementation in one script:

1. **REPL and dispatch** — `app/main.py` reads input, records history, classifies commands, and coordinates execution.
2. **Tokenization** — `app/tokenizer.py` uses explicit states to process unquoted text, quoted text, and escaped characters.
3. **Built-ins** — `app/commands.py` implements commands that need access to shell-owned state, such as `cd`, `history`, and `declare`.
4. **External processes** — executable lookup and `subprocess` calls run programs found through `PATH`.
5. **Pipelines** — `app/pipe.py` connects process output and input with `subprocess.PIPE`.
6. **Jobs and state** — dedicated modules track background processes, history, and shell-local declarations.
7. **Completion** — the `app/completer/` package integrates with readline/libedit and supports built-in, executable, path, and programmable completion.

## Project Structure

```text
.
├── app/
│   ├── completer/          # Readline and programmable completion
│   ├── main.py             # Interactive loop and command dispatch
│   ├── commands.py         # Built-in command handlers
│   ├── tokenizer.py        # State-machine tokenizer
│   ├── pipe.py             # Pipeline construction
│   ├── jobs.py             # Background job registry
│   ├── history.py          # In-memory and file-backed history
│   ├── declare.py          # Shell-local variables
│   ├── redirection.py      # Overwrite redirection helpers
│   └── append.py           # Append redirection helpers
├── codecrafters.yml        # CodeCrafters project configuration
├── pyproject.toml          # Python project metadata
├── uv.lock                 # Reproducible uv environment
└── your_program.sh         # Local launcher
```

## Current Limitations

The project implements a deliberately constrained subset of shell behavior. It currently does not support:

- POSIX-complete parsing or scripting
- command operators such as `&&`, `||`, and `;`
- command substitution, arithmetic expansion, or filename globbing
- input redirection, here-documents, or file descriptor duplication
- exported shell variables or general environment-variable expansion
- process groups and full terminal job control such as `fg` and `bg`
- aliases, functions, startup files, or a configurable prompt

Some quoting, expansion, redirection, and pipeline combinations also remain intentionally narrower than their Bash or Zsh equivalents.

## What I Learned

Building a shell turned everyday terminal behavior into concrete systems concepts. The project gave me hands-on experience with:

- designing a tokenizer as a finite-state machine
- distinguishing shell built-ins from external executables
- managing child processes and connecting their standard streams
- preserving state across commands in a long-running REPL
- implementing history, completion, variables, and background job bookkeeping
- handling the behavioral edge cases hidden behind a small command prompt

CodeCrafters provided the staged challenge and remote tests; the implementation and its organization evolved as I worked through those requirements and explored additional shell behavior.

## License

This project is available under the [MIT License](LICENSE).
