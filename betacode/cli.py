import click
import sys
from .conv import beta_to_uni, uni_to_beta

text_argument = click.argument("text", nargs=-1, type=str)
input_option = click.option(
    "--input",
    "-i",
    "input_file",
    type=click.File("r"),
    default=sys.stdin,
    help="Input file containing text to be converted.",
)
strict_option = click.option(
    "--strict",
    "-s",
    "strict",
    is_flag=True,
    default=False,
    help="Flag to disallow flexible diacritic order on input.",
)
continuous_option = click.option(
    "--continuous",
    "-c",
    "continuous",
    is_flag=True,
    help="Turn on continuous mode for repeated conversions.",
)


def get_input_string(text, input_file):
    return " ".join(text) if text else input_file.read()


@click.command()
@text_argument
@input_option
@strict_option
@continuous_option
def beta_to_uni_cli(text, input_file, strict, continuous):
    if continuous:
        while True:
            text_input = input("> ")
            click.echo(beta_to_uni(text_input, strict))
    else:
        text_input = get_input_string(text, input_file)
        click.echo(beta_to_uni(text_input, strict))


@click.command()
@text_argument
@input_option
@continuous_option
def uni_to_beta_cli(text, input_file, continuous):
    if continuous:
        while True:
            text_input = input("> ")
            click.echo(uni_to_beta(text_input))
    else:
        text_input = get_input_string(text, input_file)
        click.echo(uni_to_beta(text_input))
