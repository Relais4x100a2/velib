import click

@click.group()
def velib():
    """
    Petit outil CLI pour trouver une station velib proche de l'Ecole des chartes afin de prendre ou rendre un velib
     """

    return True


@velib.command("prendre_velib")
def prendre():
    print("Voici la station poure prendre un vélib")


@velib.command("rendre_velib")
def rendre():
    print("Voici la station pour rendre un vélib")


if __name__ == "__main__":
    velib()
