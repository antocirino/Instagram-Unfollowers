import zipfile
import os
import json

def main():
    
    # Ask if the user is from Phone or PC
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
            break
        elif choice == "n": 
            print("\nWait for the email and try again.")
            

def procedures():
    
    file_extraction()

    move_files()

    delete_files()

    json_diff()

    #remove_json()


def file_extraction():
    # Extract the zip file in the "data" folder
    zip_files = [f for f in os.listdir('data') if f.endswith('.zip')]
    if not zip_files:
        print("\n[ERROR] No zip files found in the 'data' folder.")
        return

    for zip_file in zip_files:
        zip_path = os.path.join('data', zip_file)
        extract_path = os.path.join('data', os.path.splitext(zip_file)[0])

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        #print(f"[DEBUG]File '{zip_file}' extracted successfully.")

    return

def move_files():
    # Move the JSON files from subdirectories to the "data" folder
    extracted_folders = [f for f in os.listdir('data') if os.path.isdir(os.path.join('data', f))]
    if not extracted_folders:
        print("\n[ERROR] No extracted folders found in the 'data' folder.")
        return

    for folder in extracted_folders:
        folder_path = os.path.join('data', folder)
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(root, file)
                    new_path = os.path.join('data', file)
                    os.rename(json_path, new_path)
                    #print(f"[DEBUG] File '{file}' moved successfully from '{root}' to 'data'.")


    return

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
                #print(f"[DEBUG] Deleted file: {file_path}")

    # Delete empty subdirectories
    for root, dirs, _ in os.walk(data_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                #print(f"[DEBUG] Deleted empty directory: {dir_path}")

def json_diff():
    following_path = 'data/following.json'
    followers_path = 'data/followers.json'
    followers_1_path = 'data/followers_1.json'

    if not os.path.exists(following_path):
        print("\n[ERROR] 'following.json' file not found.")
        return
    if not os.path.exists(followers_path):
        #print("\n[ERROR] 'followers.json' file not found.")
        followers_path = followers_1_path
        if not os.path.exists(followers_path):
            print("\n[ERROR] 'followers.json' file not found.")
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

    if unfollowed:
        print("\nUnfollowed users:")
        for user in unfollowed:
            print(f"- {user}")
    else:
        print("\nNo unfollowed users found.")
    

def remove_json():
    # Remove the JSON files
    for file in os.listdir('data'):
        if file.endswith('.json'):
            file_path = os.path.join('data', file)
            os.remove(file_path)
            #print(f"[DEBUG] Deleted file: {file_path}")
    
    return


if __name__ == "__main__":
    main()