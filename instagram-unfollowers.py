import zipfile
import os
import json
import argparse
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console

platform_choice = [
    Choice("phone", name="Phone"),
    Choice("pc", name="PC"),
    Choice("EXIT", name="Exit"),
]


def main():

    global args

    parser = argparse.ArgumentParser(description='Instagram\'s Unfollowers')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-q', '--quick', action='store_true', help='skip the guided procedure')
    parser.add_argument('-e', '--export', action='store_true', help='export the results to a text file')
    parser.add_argument('-t', '--threshold', action='store_true', help='enable the threshold to filter out users with more than 60k followers')

    args = parser.parse_args()

    if args.quick:
        procedures()
        return


    platform = inquirer.select(
        message="Select your platform: ",
        choices=platform_choice,
        cycle=True,
        border=True,
        invalid_message="Select an option",
        mandatory=True,
        mandatory_message="Select an option",
    ).execute()

    if platform == "phone":
        phone_onboarding()
    elif platform == "pc":
        pc_onboarding()
    elif platform == "EXIT":
        return


def phone_onboarding():
    print("\nFollow the steps below to download your Instagram data.\n")
    steps = [
        "Apri Instagram",
        "Vai nel profilo",
        "In alto a destra premere Impostazioni e attività’",
        "Vai in Centro gestione account",
        "Premere su Le tue informazioni e autorizzazioni e poi su Scarica le tue informazioni",
        "Premere su Scarica o trasferisci informazioni e seleziona Alcune delle tue informazioni",
        "Scorri fino alla sezione Contatti e spunta Follower e persone/Pagine seguite",
        "Premere su Avanti",
        "Scarica sul dispositivo",
        "Come Intervallo di date scegliere Dall’inizio.",
        "Impostare il formato su JSON e la Qualità dei contenuti multimediali su Bassa",
        "Premere su Crea file e aspettare la mail di conferma"
    ]

    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
        
    print("\n")

    guided_procedures()

def pc_onboarding():
    print("\nFollow the steps below to download your Instagram data.\n")
    steps = [
        "Visita il link https://accountscenter.instagram.com/info_and_permissions/",
        "Accedi con le tue credenziali",
        "Premi su Scarica le tue informazioni",
        "Premere su Scarica o trasferisci informazioni e seleziona Alcune delle tue informazioni",
        "Scorri fino alla sezione Contatti e spunta Follower e persone/Pagine seguite",
        "Premere su Avanti",
        "Scarica sul dispositivo",
        "Come Intervallo di date scegliere Sempre.",
        "Impostare il formato su JSON e la Qualità dei contenuti multimediali su Bassa",
        "Premere su Crea file e aspettare la mail di conferma"
    ]

    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    print("\n")

    guided_procedures()


def guided_procedures():
    
    while True:

        email = False
        try:
            email = inquirer.confirm(message="Have you received the email?", default=True, raise_keyboard_interrupt=True).execute()
        except KeyboardInterrupt:
            info_print("Process interrupted. Exiting...")
            sys.exit()

        if email:

            print("\n")
            # Alert the user if the "data" folder is not empty
            remove_precedent_files()

            print("\n1. Apri la mail e scarica il file premendo Scarica le tue informazioni.")
            print("2. Salva il file nella cartella del progetto denominata 'data'.")
            print("\n")
            
            while True:

                saved = False
                try:
                    saved = inquirer.confirm(message="Have you saved the file in the Data folder?", default=True, raise_keyboard_interrupt=True).execute()
                except KeyboardInterrupt:
                    info_print("Process interrupted. Exiting...")
                    sys.exit()

                if saved:
                    print("\n")
                    procedures()
                    break
                else:
                    print("\n")
                    info_print("Save the file in the Data folder and try again.")
            break
        else:
            info_print("Wait for the email and try again.")
            print("\n")

            

def procedures():
    
    # Extract the zip file in the "data" folder
    file_extraction()

    # Move the JSON files from subdirectories to the "data" folder
    move_files()

    # Delete unnecessary files
    delete_files()

    # Find the difference between the two lists
    json_diff()


def remove_precedent_files(): 

    # Verify if the "data" folder has files and alert the user
    if os.path.exists('data') and os.listdir('data'):
        while True:

            delete = False
            delete = inquirer.confirm(message="The 'Data' folder is not empty. To proceed, the Data folder must be empty. Do you want to delete the files?").execute()

            if delete:
                # If the "data" folder has files or subdirectories or both, delete them
                for root, dirs, files in os.walk('data', topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        debug_print(f"Deleted file: {file_path}")
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        os.rmdir(dir_path)
                        debug_print(f"Deleted directory: {dir_path}")

                break
            else:
                return


def file_extraction():
    # Extract the zip file in the "data" folder
    zip_files = [f for f in os.listdir('data') if f.endswith('.zip')]
    if not zip_files:
        err_print("No zip files found in the 'data' folder.")
        return

    for zip_file in zip_files:
        zip_path = os.path.join('data', zip_file)
        extract_path = os.path.join('data', os.path.splitext(zip_file)[0])

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        debug_print(f"File '{zip_file}' extracted successfully.")


def move_files():
    # Move the JSON files from subdirectories to the "data" folder
    extracted_folders = [f for f in os.listdir('data') if os.path.isdir(os.path.join('data', f))]
    if not extracted_folders:
        err_print("No extracted folders found in the 'data' folder.")
        return

    for folder in extracted_folders:
        folder_path = os.path.join('data', folder)
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(root, file)
                    new_path = os.path.join('data', file)
                    os.rename(json_path, new_path)
                    debug_print(f"File '{file}' moved successfully from '{root}' to 'data'.")



def delete_files():
    # Delete unnecessary files
    # The only files needed are:
    # - followers.json
    # - followers_1.json
    # - following.json
    data_folder = 'data'
    required_files = {'followers.json', 'following.json', 'followers_1.json'}

    for root, _, files in os.walk(data_folder):
        for file in files:
            if file not in required_files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                debug_print(f"Deleted file: {file_path}")

    # Delete empty subdirectories
    for root, dirs, _ in os.walk(data_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                debug_print(f"Deleted empty directory: {dir_path}")
    
    
def get_follower_count(username):
    headers = {
        'x-ig-app-id': '936619743392459'
    }

    url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        err_print(f"You have reached the maximum number of requests. Please try again in a few hours.")
        info_print("You can run python3 instagram-unfollowers.py without -t to disable the threshold and check the users that don't follow you back.")
        sys.exit()
        return 0
    except KeyError:
        err_print(f"Unexpected response structure for user {username}")
        return 0
    
def check_followers_number(followers_number):
    # 60k is the threshold, you can change it to any number you want
    return followers_number >= 60000

def json_diff():
    following_path = 'data/following.json'
    followers_path = 'data/followers.json'
    followers_1_path = 'data/followers_1.json'

    if not os.path.exists(following_path):
        err_print("'following.json' file is not present in the 'data' folder.")
        return
    if not os.path.exists(followers_path):
        followers_path = followers_1_path
        if not os.path.exists(followers_path):
            err_print("No JSON files found in the 'data' folder.")
            return
            
    # Load JSON data
    with open(following_path, 'r') as file:
        following_data = json.load(file)
    with open(followers_path, 'r') as file:
        followers_data = json.load(file)

    # Extract the lists of usernames
    following_list = [item['string_list_data'][0]['value'] for item in following_data['relationships_following']]
    followers_list = [item['string_list_data'][0]['value'] for item in followers_data]

    # Find the difference (people who unfollowed)
    unfollowed = [user for user in following_list if user not in followers_list]

    # Filter out users with more than 60k followers using multithreading
    if args.threshold:
        info_print("Filtering out users with more than 60k followers...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(get_follower_count, unfollowed))
        
        unfollowed = [user for user, count in zip(unfollowed, results) if not check_followers_number(count)]

    if unfollowed:
        if args.export:
            download_results(unfollowed)
        else:
            print("Users that don't follow you back:")
            for user in unfollowed:
                print(f"- {user}")
    else:
        print("\nNo users that don't follow you back found.")

def download_results(unfollowed):
    # Download the results as a text file
    with open('data/unfollowers.txt', 'w') as file:
        for user in unfollowed:
            file.write(f"{user}\n")
    print(f"\nResults downloaded to 'unfollowers.txt' in the 'data' folder.")
    

def remove_json():
    # Remove the JSON files from the "data" folder
    for file in os.listdir('data'):
        if file.endswith('.json'):
            file_path = os.path.join('data', file)
            os.remove(file_path)
            debug_print(f"Deleted file: {file_path}")


def err_print(msg):
    console = Console()
    console.print(f"[bold white on red] ERROR [/bold white on red] {msg}")


def debug_print(msg):
    if args.debug:
        console = Console()
        console.print(f"[bold black on white] DEBUG [/bold black on white] {msg}")

def info_print(msg):
    console = Console()
    console.print(f"[bold white on blue] INFO [/bold white on blue] {msg}")

def banner():
    font = r"""
 _____ _____       _   _        __      _ _                            
|_   _|  __ \     | | | |      / _|    | | |                           
  | | | |  \/_____| | | |_ __ | |_ ___ | | | _____      _____ _ __ ___ 
  | | | | _|______| | | | '_ \|  _/ _ \| | |/ _ \ \ /\ / / _ \ '__/ __|
 _| |_| |_\ \     | |_| | | | | || (_) | | | (_) \ V  V /  __/ |  \__ \
 \___/ \____/      \___/|_| |_|_| \___/|_|_|\___/ \_/\_/ \___|_|  |___/ """
    print(font)
    print("\t\tCopyright (c) 2025 Antonio Cirino\n")

if __name__ == "__main__":
    banner()
    main()