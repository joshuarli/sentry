from __future__ import annotations

import collections
import subprocess
import sys
from collections.abc import Sequence

from tools.mypy_helpers.mypy_output import InvalidMypyOutput, parse_mypy_output


def _by_count_then_name(item: tuple[str, int]) -> tuple[int, str]:
    filename, count = item
    return (count, filename)


def main(argv: Sequence[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    out = subprocess.run(
        (sys.executable, "-m", "tools.mypy_helpers.mypy_without_ignores", *args),
        capture_output=True,
    )
    counts: collections.Counter[str] = collections.Counter()
    try:
        run = parse_mypy_output(out.stdout, out.stderr, out.returncode)
    except InvalidMypyOutput as exc:
        print(str(exc), file=sys.stderr)
        return 2
    for diagnostic in run.errors:
        if diagnostic.filename is None:
            print("mypy reported an error without a source filename", file=sys.stderr)
            return 2
        counts[diagnostic.filename] += 1

    for filename, count in sorted(counts.items(), key=_by_count_then_name):
        print(f"{count}\t{filename}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
