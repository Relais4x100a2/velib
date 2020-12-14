import click
import requests


@click.group()
def velib():
    """
    Petit outil CLI pour trouver une station velib proche de l'École des chartes afin de prendre ou rendre un velib
    """
    return True


@velib.command("prendre_velib")
def prendre()
    print ("Voici la station pour prendre un velib")
   


@velib.command("rendre_velib")
def rendre():
    print("Voici la station pour rendre un velib")


if __name__ == "__main__":
    velib()
