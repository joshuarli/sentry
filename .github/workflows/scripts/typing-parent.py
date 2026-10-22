from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

POLICY_PATHS = (
    "tools/mypy_helpers/typing_campaign.py",
    "tools/mypy_helpers/mypy_output.py",
    "tools/mypy_helpers/mypy_config.py",
    "tools/mypy_helpers/config_sections.py",
)
ZERO_SHA = re.compile(r"^0+$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


class Arguments(Namespace):
    event: str
    pull_request_base: str
    push_before: str
    repository: Path
    output: Path


def git(
    repository: Path,
    *arguments: str,
    index: Path | None = None,
    input_text: str | None = None,
) -> str:
    environment = os.environ.copy()
    if index is not None:
        environment["GIT_INDEX_FILE"] = str(index)
    if arguments[0] == "commit-tree":
        environment.setdefault("GIT_AUTHOR_NAME", "Typing guard")
        environment.setdefault("GIT_AUTHOR_EMAIL", "typing-guard@example.invalid")
        environment.setdefault("GIT_COMMITTER_NAME", "Typing guard")
        environment.setdefault("GIT_COMMITTER_EMAIL", "typing-guard@example.invalid")
    result = subprocess.run(
        ("git", *arguments),
        cwd=repository,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
        input=input_text,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(arguments)} failed")
    return result.stdout.strip()


def select_parent(
    event_name: str,
    pull_request_base: str,
    push_before: str,
    first_parent: str,
) -> str:
    if event_name == "pull_request":
        selected = pull_request_base
    elif event_name == "push":
        selected = "" if ZERO_SHA.fullmatch(push_before) else push_before
    elif event_name == "workflow_dispatch":
        selected = ""
    else:
        raise RuntimeError(f"unsupported workflow event for typing guard: {event_name}")
    if not selected:
        selected = first_parent
    if not COMMIT_SHA.fullmatch(selected):
        raise RuntimeError("typing guard parent is missing or is not a full commit SHA")
    return selected


def ensure_commit(repository: Path, commit: str) -> str:
    try:
        resolved = git(repository, "rev-parse", "--verify", f"{commit}^{{commit}}")
    except RuntimeError:
        git(repository, "fetch", "--no-tags", "--depth=1", "origin", commit)
        resolved = git(repository, "rev-parse", "--verify", f"{commit}^{{commit}}")
    if resolved != commit:
        raise RuntimeError("typing guard parent did not resolve to the selected commit")
    return resolved


def needs_bootstrap(repository: Path, parent: str) -> bool:
    for path in POLICY_PATHS:
        try:
            git(repository, "cat-file", "-e", f"{parent}:{path}")
        except RuntimeError:
            return True
    return False


def bootstrap_parent(repository: Path, parent: str, candidate: str, index: Path) -> str:
    git(repository, "read-tree", parent, index=index)
    for path in POLICY_PATHS:
        entry = git(repository, "ls-tree", candidate, "--", path)
        if not entry:
            raise RuntimeError(f"candidate is missing evaluator policy dependency {path}")
        metadata, listed_path = entry.split("\t", 1)
        mode, object_type, object_id = metadata.split()
        if listed_path != path or object_type != "blob":
            raise RuntimeError(f"candidate evaluator policy dependency is not a file: {path}")
        git(
            repository,
            "update-index",
            "--add",
            "--cacheinfo",
            f"{mode},{object_id},{path}",
            index=index,
        )
    tree = git(repository, "write-tree", index=index)
    return git(
        repository,
        "commit-tree",
        tree,
        "-p",
        parent,
        input_text="Typing evaluator bootstrap for pre-evaluator parent",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    parser.add_argument("--pull-request-base", default="")
    parser.add_argument("--push-before", default="")
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(namespace=Arguments())
    try:
        repository = arguments.repository.resolve()
        scratch = repository / ".work" / "tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        candidate = git(repository, "rev-parse", "--verify", "HEAD^{commit}")
        first_parent = ""
        if arguments.event == "workflow_dispatch" or (
            arguments.event == "push" and ZERO_SHA.fullmatch(arguments.push_before)
        ):
            candidate_parents = git(
                repository, "show", "-s", "--format=%P", candidate
            ).split()
            if not candidate_parents:
                raise RuntimeError("candidate commit has no first parent")
            first_parent = candidate_parents[0]
        selected = select_parent(
            arguments.event,
            arguments.pull_request_base,
            arguments.push_before,
            first_parent,
        )
        ensure_commit(repository, selected)
        bootstrap = needs_bootstrap(repository, selected)
        parent = selected
        if bootstrap:
            index = scratch / f"typing-parent-{os.getpid()}.index"
            try:
                parent = bootstrap_parent(repository, selected, candidate, index)
            finally:
                index.unlink(missing_ok=True)
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        with arguments.output.open("a", encoding="utf-8") as output:
            output.write(f"parent={parent}\n")
            output.write(f"selected_parent={selected}\n")
            output.write(f"bootstrap={'true' if bootstrap else 'false'}\n")
        print(
            f"typing guard parent: {parent}"
            + (f" (bootstrap from {selected})" if bootstrap else "")
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"typing guard parent selection failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
