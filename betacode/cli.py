"""
Command line entry point for converting betacode and unicode text.
"""

import argparse
import dataclasses
import enum
import functools
import pathlib
import sys
from collections.abc import Callable, Sequence

from . import beta_to_uni, uni_to_beta

ConvertFn = Callable[[str], str]


class Direction(enum.Enum):
    TO_UNICODE = "to-unicode"
    TO_BETA = "to-beta"


@dataclasses.dataclass(frozen=True)
class CliArgs:
    direction: Direction
    strict: bool
    file: pathlib.Path | None
    text: str | None
    interactive: bool


def _build_parser() -> argparse.ArgumentParser:
    def add_input_arguments(parser: argparse.ArgumentParser) -> None:
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-f", "--file", type=pathlib.Path, help="Path to a file to convert.")
        group.add_argument(
            "-t", "--text", help="Raw text to convert, given directly on the command line."
        )
        group.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="Start a continuous, REPL-like session. Each line entered is converted and "
            "printed.",
        )

    parser = argparse.ArgumentParser(
        prog="betacode",
        description="Convert text between betacode and unicode.",
    )
    subparsers = parser.add_subparsers(dest="direction", required=True)

    to_unicode = subparsers.add_parser(
        Direction.TO_UNICODE.value, help="Convert betacode to unicode."
    )
    to_unicode.add_argument(
        "--strict",
        action="store_true",
        help="Only accept the canonical diacritic order defined by the TLG Beta Code Manual.",
    )
    add_input_arguments(to_unicode)

    to_beta = subparsers.add_parser(Direction.TO_BETA.value, help="Convert unicode to betacode.")
    add_input_arguments(to_beta)

    return parser


def _parse_args(argv: Sequence[str] | None) -> CliArgs:
    parser = _build_parser()
    namespace = parser.parse_args(argv)

    return CliArgs(
        direction=Direction(namespace.direction),
        strict=getattr(namespace, "strict", False),
        file=namespace.file,
        text=namespace.text,
        interactive=namespace.interactive,
    )


def _run_interactive(convert: ConvertFn) -> None:
    print(
        "Entering continuous mode. Press Ctrl-D (or Ctrl-Z on Windows) to exit.", file=sys.stderr
    )
    while True:
        try:
            line = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print(file=sys.stderr)
            return

        print(convert(line))


def main(argv: Sequence[str] | None = None) -> None:
    args = _parse_args(argv)

    convert: ConvertFn
    if args.direction is Direction.TO_UNICODE:
        convert = functools.partial(beta_to_uni, strict=args.strict)
    else:
        convert = uni_to_beta

    if args.interactive:
        _run_interactive(convert)
    elif args.file is not None:
        text = args.file.read_text(encoding="utf-8")
        print(convert(text), end="")
    else:
        print(convert(args.text))


if __name__ == "__main__":
    main()
