from .conv import beta_to_uni, uni_to_beta
import click


@click.command()
@click.argument("text", nargs=-1, type=str)
@click.option(
    "--strict",
    "-s",
    "strict",
    is_flag=True,
    default=False,
    help="Flag to disallow flexible diacritic order on input.",
)
def beta_to_uni_cli(text, strict):
    click.echo(beta_to_uni(" ".join(text), strict))


@click.command()
@click.argument("text", nargs=-1, type=str)
def uni_to_beta_cli(text):
    click.echo(uni_to_beta(" ".join(text)))
