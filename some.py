#!/usr/bin/env python3.6

"""some -- more than less, but less than more.

some is a pager… sometimes. If the input is less than one screen long,
some will print it directly to the terminal; otherwise, it will display
it using whatever pager is configured.
"""


import errno
import itertools
import os
import shutil
import subprocess
import sys
from typing import cast, Iterable, Optional, Sequence, TextIO


def direct_write(lines: Sequence[str]) -> None:
    """Print some lines of text.

    The lines are assumed to end with newlines; no newlines will be
    added, apart from a final newline at the end of the output if there
    isn't one already -- though this is intended exclusively as a
    workaround for bad input, and should not be relied upon.
    """
    # If there are no lines, or the only line is an empty string,
    # there's nothing to print!
    if lines and lines[-1]:
        if lines[-1][-1] == "\n":
            end = ""
        else:
            end = "\n"
        print("".join(lines), end=end)


def page(lines: Iterable[str], pager: Optional[str] = None) -> None:
    """Print some lines of text via a pager.

    If not specified, the pager to use will be automatically guessed
    from the user's environment (i.e. the $PAGER environment variable).
    If that's not found, a sensible default will be used. If no pager is
    available, a warning will be printed.
    """
    if pager is None:
        pager = cast(str, os.environ.get("PAGER", "less"))

    cmd = [pager]

    if pager.split(os.sep)[-1] == "less":
        # -R: interpret colour escape codes
        # +F: don't exit if the output fits on one screen
        # +X: emit magic init/deinit codes to clear the screen
        cmd.extend(["-R", "-+F", "-+X"])

    # TODO: make output to the pager faster.
    try:
        pager_proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True
        )
    except FileNotFoundError:
        print("No pager available :(")
        return

    for line in lines:
        try:
            pager_proc.stdin.write(line)
        except IOError as e:
            if e.errno == errno.EPIPE:
                # Pager exited.
                break
            else:
                raise

    pager_proc.communicate()


def some(file: TextIO, reserved_lines: int = 3) -> None:
    """Put the contents of a file into stdout, maybe via a pager.

    If less screen space is available than some thinks (e.g. output will
    be immediately pushed off the screen by a shell prompt), the
    `reserved_lines` argument can be used to decrease the number of
    lines that will be printed without invoking a pager. By default,
    some will try to avoid filling the *entire* screen with unpaged
    output -- this can be disabled by passing `reserved_lines=0`.
    """
    terminal_height = shutil.get_terminal_size().lines
    usable_height = max(terminal_height - reserved_lines, 0)

    all_lines = iter(file.readline, "")

    the_lines = list(itertools.islice(all_lines, terminal_height + 1))

    if len(the_lines) > usable_height:
        page(itertools.chain(the_lines, all_lines))
    else:
        direct_write(the_lines)


def main() -> None:
    # TODO: support paging of files.
    if len(sys.argv) > 1:
        print(
            "some does not yet support paging files from the command line.",
            file=sys.stderr,
        )
        sys.exit(1)
    some(sys.stdin)


if __name__ == "__main__":
    main()
