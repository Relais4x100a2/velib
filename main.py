import click
import requests


@click.group()
def velib():
    """
    Petit outil CLI pour trouver une station velib proche de l'École des chartes afin de prendre ou rendre un velib
    """
    return True


@velib.command("prendre_velib")
@click.argument("distance", type=int, default="250")
@click.option("--mechanic", "-m", is_flag=True, default=None, help="pour un vélib mécanique")
@click.option("--electric", "-e", is_flag=True, default=None, help="pour un vélib éléctrique")
def prendre(distance, mechanic=None, electric=None):

    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes&geofilter.distance=48.8673316%2C2.3374734%2C{}&timezone=Europe%2FParis".format(
        distance)
    r = requests.get(url)
    data = r.json()

    print("Nous vous conseillons de prendre un vélib à une de ces stations : ")
    for station in data["records"]:

        if mechanic:
            if station["fields"]["mechanical"] > 1:
                print(" - A {dist} mètres de l'Ecole, la station {nom} où il y a {num_velo_m} vélos mécaniques "
                      "à {heure}h{minute}.".format(
                        dist=station["fields"]["dist"][:3],
                        nom=station["fields"]["name"],
                        num_velo_m=station["fields"]["mechanical"],
                        heure=station["record_timestamp"][11:13],
                        minute=station["record_timestamp"][14:16]
                        ))

        elif electric:
            if station["fields"]["ebike"] > 1:
                print(" - A {dist} mètres de l'Ecole, la station {nom} où il y a {num_velo_e} vélos électriques "
                      "à {heure}h{minute}.".format(
                        dist=station["fields"]["dist"][:3],
                        nom=station["fields"]["name"],
                        num_velo_e=station["fields"]["ebike"],
                        heure=station["record_timestamp"][11:13],
                        minute=station["record_timestamp"][14:16]
                        ))

        elif station["fields"]["numbikesavailable"] > 1:
            print(" - A {dist} mètres de l'Ecole, la station {nom} où il y a {num_velo} vélos "
                  "à {heure}h{minute}.".format(
                    dist=station["fields"]["dist"][:3],
                    nom=station["fields"]["name"],
                    num_velo=station["fields"]["numbikesavailable"],
                    heure=station["record_timestamp"][11:13],
                    minute=station["record_timestamp"][14:16]
                    ))


@velib.command("rendre_velib")
def rendre():
    print("Voici la station pour rendre un velib")


if __name__ == "__main__":
    velib()