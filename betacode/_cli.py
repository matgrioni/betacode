"""
Command line entry point for converting betacode and unicode text.
"""

import argparse
from collections.abc import Callable
from dataclasses import dataclass
import enum
import pathlib
import sys

from . import beta_to_uni, uni_to_beta


class Direction(enum.Enum):
    """Which way to convert text: betacode to unicode, or unicode to betacode."""

    TO_UNICODE = "to-unicode"
    TO_BETA = "to-beta"


@dataclass(frozen=True)
class TextInput:
    """Input given directly on the command line."""

    text: str


@dataclass(frozen=True)
class FileInput:
    """Input read from the contents of a file."""

    path: pathlib.Path


@dataclass(frozen=True)
class InteractiveInput:
    """Input read line by line from a continuous, REPL-like session."""


Input = TextInput | FileInput | InteractiveInput


@dataclass(frozen=True)
class CliArgs:
    """The parsed and validated command line arguments."""

    direction: Direction
    strict: bool
    input: Input


def _parse_args() -> CliArgs:
    """
    Parse and validate the process's command line arguments.

    Returns:
        The parsed arguments, including which single input source was given.
    """

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

    parsed = parser.parse_args()

    return CliArgs(
        direction=Direction(parsed.direction),
        strict=getattr(parsed, "strict", False),
        input=_parse_input(parsed),
    )


def _parse_input(parsed: argparse.Namespace) -> Input:
    """
    Translate the raw, mutually exclusive input flags into a single input source.

    Args:
        parsed: The parsed argparse namespace, with `file`, `text`, and `interactive`
            attributes.

    Returns:
        The one input source that was given.
    """
    if parsed.interactive:
        return InteractiveInput()
    if parsed.file is not None:
        return FileInput(parsed.file)
    if parsed.text is not None:
        return TextInput(parsed.text)

    raise ValueError("one of --file, --text, or --interactive must be given")


def _run_interactive(convert: Callable[[str], str]) -> None:
    """
    Run a continuous, REPL-like session, converting and printing each line entered.

    Args:
        convert: The conversion function to apply to each line, until the user exits with
            Ctrl-D (or Ctrl-Z on Windows).
    """
    print("Entering continuous mode. Press Ctrl-D (or Ctrl-Z on Windows) to exit.", file=sys.stderr)
    while True:
        try:
            line = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print("Exiting interactive loop...", file=sys.stderr)
            return

        print(convert(line))


def main() -> None:
    """
    Entry point for the `betacode` console script.

    Parses the command line arguments, then converts and prints the requested input using
    either `beta_to_uni` or `uni_to_beta`, depending on the given direction.
    """
    args = _parse_args()

    convert: Callable[[str], str]
    if args.direction is Direction.TO_UNICODE:
        strict = args.strict

        def convert(text: str) -> str:
            return beta_to_uni(text, strict=strict)

    else:
        convert = uni_to_beta

    match args.input:
        case InteractiveInput():
            _run_interactive(convert)
        case FileInput(path):
            print(convert(path.read_text(encoding="utf-8")), end="")
        case TextInput(text):
            print(convert(text))


if __name__ == "__main__":
    main()
