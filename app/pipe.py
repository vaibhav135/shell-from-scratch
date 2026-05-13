import subprocess


def handle_piping(
    cmd: list[str],
    proc_cache: subprocess.Popen[str] | None,
    prev_cmd_ouput: str,
    is_last_idx: bool,
) -> subprocess.Popen[str]:
    cmd = [c.replace('"', "") for c in cmd]

    if not proc_cache and not is_last_idx:
        proc_cache = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
    elif proc_cache:
        if is_last_idx:
            proc_cache = subprocess.Popen(
                cmd,
                stdin=proc_cache.stdout,
                encoding="utf-8",
            )

        else:
            proc_cache = subprocess.Popen(
                cmd,
                stdin=proc_cache.stdout,
                stdout=subprocess.PIPE,
                encoding="utf-8",
            )
    else:
        proc_cache = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            encoding="utf-8",
        )

        if prev_cmd_ouput and proc_cache.stdin:
            proc_cache.stdin.write(prev_cmd_ouput + "\n")
            proc_cache.stdin.flush()

    return proc_cache
