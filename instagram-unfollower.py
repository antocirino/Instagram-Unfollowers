def main():
    
    # Ask if the user is from Phone or PC
    while True:
        print("Are you using a Phone or a PC?")
        print("1. Phone")
        print("2. PC")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            phone_procedure()
            break
        elif choice == 2:
            pc_procedure()
            break
        elif choice == 3:
            return
        else:
            print("Invalid choice. Please try again.")


def phone_procedure():
    print("\n")
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

    while True:
        print("\nHave you received the email? (y/n)")
        choice = input("Enter your choice: ")

        if choice == "y":
            print("1. Apri la mail e scarica il file premendo Scarica le tue informazioni.")
            print("2. Salva il file nella cartella del progetto denominata 'data'.")
            break
        elif choice == "n": 
            print("\nWait for the email and try again.")


    return

def pc_procedure():
    return

if __name__ == "__main__":
    main()