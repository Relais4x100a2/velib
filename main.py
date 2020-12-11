import click
import requests
from terminaltables import AsciiTable
from operator import itemgetter

@click.group()
def velib():
    """
    Petit outil CLI pour trouver une station velib proche de l'École des chartes afin de prendre ou rendre un velib
    """
    return True

@velib.command("prendre_velib")
def prendre():
    print("Voici la station pour prendre un velib")

@velib.command("rendre_velib")
@click.option("-distance", "distlimit", type=int, default="250")
@click.option("-libre", "lib", is_flag=True, default=False, help="Tri en fonction du nb de places disponibles")
def rendre(distlimit, lib):
    #   URL de recherche API VELIB - STATIONS se situant à moins de 250m (par défaut) de l'école des Chartes
    url= "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes&geofilter.distance=48.8673316%2C2.3374734%2C{}".format(
            distlimit)
    #   Avec la variable R, on passera une requête GET sur URL qui est le paramètre de la fonction"""
    r = requests.get(url)
    #  Avec la variable DATA, on récupéra la réponse(le body) au format JSON """
    data = r.json()
    resultat=[]

    for station in data["records"]:
         # définition des éléments qu'on souhaite récupérer pour chaque item
         item = station["fields"]
         # on définit d'abord une variable "item" qui nous permettra d'aller chercher chaque qu'on souhaite récupérer :
         retour_ok = item["is_returning"]
         name = item["name"]
         free_place = item["numdocksavailable"]
         distance = round(float(item["dist"]))
         coord_geo = item["coordonnees_geo"]
         capacity = item["capacity"]
         per_free_place = round(free_place / capacity * 100)

         if retour_ok == "OUI":
             if free_place > 0:
                 resultat.append([name, free_place, per_free_place, distance, coord_geo])
             resultat = sorted(resultat, key=itemgetter(3))

    if len(resultat) == 0:
        print("Oups ! Il n'y a plus de places de libre.\n"
              "Faîtes une nouvelle requête en passant le paramètre -distance\n"
              "Par exemple :\n"
              "python main.py rendre_velib -distance 500")

    else:
        if lib:
            resultat = sorted(resultat, key=itemgetter(1,2), reverse=True)

        header = [["Nom de la station","Nb de places libres","Taux de places libres","Proximité de l'école","Coordonnées WGS84"]]
        table = AsciiTable(header+resultat)
        table.justify_columns[1] = 'right'
        table.justify_columns[2] = 'center'
        table.justify_columns[3] = 'right'
        print(table.table)

if __name__ == "__main__":
    velib()
