import zipfile
import os
import json
import argparse
import requests
from bs4 import BeautifulSoup
import concurrent.futures

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
                                                     
    while True:
        print("Are you using a Phone or a PC?")
        print("1. Phone")
        print("2. PC")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            phone_onboarding()
            break
        elif choice == 2:
            pc_onboarding()
            break
        elif choice == 3:
            return
        else:
            print("Invalid choice. Please try again.")
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
        "Come Intervallo di date scegliere Dall’inizio.",
        "Impostare il formato su JSON e la Qualità dei contenuti multimediali su Bassa",
        "Premere su Crea file e aspettare la mail di conferma"
    ]

    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")

    guided_procedures()


def guided_procedures():
    while True:
        print("\nHave you received the email? (y/n)")
        choice = input("Enter your choice: ")

        if choice == "y":
            print("\n1. Apri la mail e scarica il file premendo Scarica le tue informazioni.")
            print("2. Salva il file nella cartella del progetto denominata 'data'.")
            
            while True:
                print("\nHave you saved the file in the 'data' folder? (y/n)")
                choice = input("Enter your choice: ")

                if choice == "y":
                    procedures()
                    break
                elif choice == "n":
                    print("\nSave the file in the 'data' folder and try again.")
                elif choice == "q" or choice == "exit":
                    return
                else:
                    print("Invalid choice. Please try again.")
            break
        elif choice == "n": 
            print("\nWait for the email and try again.")
        elif choice == "q" or choice == "exit":
            return
        else:
            print("Invalid choice. Please try again.")
            

def procedures():
    
    # Extract the zip file in the "data" folder
    file_extraction()

    # Move the JSON files from subdirectories to the "data" folder
    move_files()

    # Delete unnecessary files
    delete_files()

    # Find the difference between the two lists
    json_diff()


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

def instagram_followers(username):

    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

    response = requests.get(url, headers=headers)    
    soup = BeautifulSoup(response.text, 'html.parser')
    followers = soup.find('meta', property='og:description')
    
    if followers:

        # If the string contains K (1000) or M (1,000,000) then convert it to an integer
        if "K" in followers['content']:
            followers['content'] = followers['content'].replace("K", "000").replace(".", "")
        if "M" in followers['content']:
            followers['content'] = followers['content'].replace("M", "000000").replace(".", "")

        # If the string contains comma or dot then remove them
        followers['content'] = followers['content'].replace(",", "")
        followers['content'] = followers['content'].replace(".", "")

        return followers['content'].split(" ")[0]
    else:
        return -1
    
def check_followers_number(followers_number, threshold):
    if followers_number >= 60000:
        return True
    else:
        return False
    
def filter_unfollowed(user):
    followers_number = int(instagram_followers(user))

    if followers_number == -1:
        err_print(f"Error fetching followers number for user '{user}'.")
        return

    if not check_followers_number(followers_number, args.threshold):
        return user
    return None

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

    if args.threshold:
        # Filter out users with more than n followers
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(filter_unfollowed, unfollowed))
        unfollowed = [user for user in results if user]


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
    RED = "\33[91m"
    END = "\033[0m"
    font =f"""{RED}\n[ERROR] {msg}{END}"""
    print(font)

def debug_print(msg):
    if args.debug:
        CYAN = "\033[36m"
        END = "\033[0m"
        font =f"""{CYAN}\n[DEBUG] {msg}{END}"""
        print(font)


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