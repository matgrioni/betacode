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


def get_input_string(text, input_file):
    return " ".join(text) if text else input_file.read()


@click.command()
@text_argument
@input_option
@strict_option
def beta_to_uni_cli(text, input_file, strict):
    text_input = get_input_string(text, input_file)
    click.echo(beta_to_uni(text_input, strict))


@click.command()
@text_argument
@input_option
def uni_to_beta_cli(text, input_file):
    text_input = get_input_string(text, input_file)
    click.echo(uni_to_beta(text_input))
