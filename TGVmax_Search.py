from turtle import update
import urllib.request, json
from urllib.parse import quote
import argparse
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_config(config_path):
    with open(config_path) as f:
        config = yaml.load(f, Loader=SafeLoader)
        return config

def prepare_url(startdate, enddate, origin, destination):
    url = f"https://sncf-simulateur-api-prod.azurewebsites.net/api/RailAvailability/Search/"
    url += quote(origin) + "/"                # LYON%20(gares%20intramuros)/
    url += quote(destination) + "/"            # PARIS%20(intramuros)/
    url += startdate + "/"              # 2022-07-07T00:00:00/
    url += enddate                      # 2022-07-07T23:59:59
    return url

def check_info(origin,destination,date,config):
    Stations = config.get('Stations')
    if origin not in Stations:
        print(f"{bcolors.FAIL} /!\ ", origin, f" n'est pas dans la liste des stations TGVMax. Veuillez vérifier l'orthographe et sélectionner une gare éligible {bcolors.ENDC}")
        return True
    if destination not in Stations:
        print(f"{bcolors.FAIL} /!\ ", destination, f" n'est pas dans la liste des stations TGVMax. Veuillez vérifier l'orthographe et sélectionner une gare éligible {bcolors.ENDC}")
        return True
    current_date = datetime.now().strftime("%Y-%m-%d")
    if date < current_date:
        print(f"{bcolors.FAIL} /!\ la date sélectionnée ", date, f" est passée. Veuillez sélectionner une date future {bcolors.ENDC}")
        return True
    return False

def iterate_config(config):

    travels = config.get('Travels')
    for travel_key in travels:
        travel = travels.get(travel_key)

        origin = travel.get('origin')
        destination = travel.get('destination')
        date = travel.get('date').strftime("%Y-%m-%d")

        if check_info(origin,destination,date,config) == False:
            search_train(origin, destination, date)


def parse_data(data):
    available_TGVMax = []
    for train in data:
        if train.get('availableSeatsCount') > 0:
            available_TGVMax.append({"train" : train.get('train'), "seats" : train.get('availableSeatsCount'),
                "departure" : train.get('departureDateTime'), "arrival" : train.get('arrivalDateTime')})

    last_departure = data[-1].get("departureDateTime")
    return available_TGVMax, last_departure


def search_train(origin,destination,date):
    
    available_TGVMAX_list = []
    number_of_trains =0

    startdate = date + "T00:00:00"
    enddate = date + "T23:59:59"
    
    while True:

        url = prepare_url(startdate, enddate, origin, destination)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        number_of_trains += len(data)
    
        if len(data)==0: 
            break
    
        else :
            available_TGVMax,last_departure = parse_data(data)
            available_TGVMAX_list += available_TGVMax

            last_departure_time = datetime.strptime(last_departure, '%Y-%m-%dT%H:%M:%S')
            updated_time = last_departure_time + timedelta(minutes = 1)
            startdate = updated_time.strftime("%Y-%m-%dT%H:%M:%S")

    if number_of_trains==0:
        print(f"{bcolors.FAIL} /!\ Pas de trains MAX trouvé de ", origin, " à ",destination , " le ",date , f". {bcolors.ENDC}")
    elif len(available_TGVMax)==0:
        print(f" {bcolors.WARNING}Pas de places TGV Max trouvées de ", origin, " à ",destination , " le ",date , " (sur ", number_of_trains, f" trains MAX trouvés){bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}", len(available_TGVMAX_list), "train(s) TGV Max disponible(s) de ", origin, " à ",destination , " le ",date , " (sur ", number_of_trains, f" trains MAX trouvés){bcolors.ENDC}")
    for tgv in available_TGVMAX_list:
        print(f" {bcolors.OKGREEN} ------> ", tgv.get('seats'), " places disponibles à bord du train ", tgv.get('train'), " partant à ", tgv.get('departure')[11:], f" {bcolors.ENDC}")

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='search for TGVMax trains availability')
    parser.add_argument('-c','--config', type=str, metavar='C', help='path to config file', required='True')
    args = parser.parse_args()

    # Load config and start searching
    config = load_config(args.config)
    iterate_config(config)

if __name__ == '__main__':
    main()