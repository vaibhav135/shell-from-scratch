import subprocess


def handle_piping(
    arg: str,
    proc_cache: subprocess.Popen[str] | None,
    prev_cmd_ouput: str,
    is_last_idx: bool,
) -> subprocess.Popen[str]:
    cmd = arg.strip().split(" ")
    if proc_cache is None and not prev_cmd_ouput:
        proc_cache = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf-8")
    elif proc_cache:
        proc_cache = subprocess.Popen(
            cmd,
            stdin=proc_cache.stdout,
            encoding="utf-8",
        )
    else:
        proc_cache = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            encoding="utf-8",
        )

        if proc_cache.stdin:
            proc_cache.stdin.write(prev_cmd_ouput + "\n")
            proc_cache.stdin.flush()

    return proc_cache
