import os
import time
import webbrowser
import platform
from colorama import Fore, Style, init

def slow_print(text, color, delay=0.05):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    init(autoreset=True)
    clear_screen()

    # First ASCII Art in Red
    first_art = """
    ██████╗ ██████╗  ██████╗ ███████╗███████╗██╗   ██╗
    ██╔══██╗██╔══██╗██╔═══██╗╚══███╔╝╚══███╔╝╚██╗ ██╔╝
    ██████╔╝██████╔╝██║   ██║  ███╔╝   ███╔╝  ╚████╔╝ 
    ██╔═══╝ ██╔══██╗██║   ██║ ███╔╝   ███╔╝    ╚██╔╝  
    ██║     ██║  ██║╚██████╔╝███████╗███████╗   ██║   
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
    """
    slow_print(first_art, Fore.RED, 0.002)
    time.sleep(2)
    clear_screen()

    # Second ASCII Art in Purple
    second_art = """
    ██████╗  ██╗ ██████╗  ██████╗ ██╗  ██╗    ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗    
    ██╔══██╗███║██╔════╝ ██╔════╝ ██║  ██║    ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝    
    ██████╔╝╚██║███████╗ ███████╗ ███████║    ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝     
    ██╔═══╝  ██║██╔═══██╗██╔═══██╗╚════██║    ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗     
    ██║      ██║╚██████╔╝╚██████╔╝     ██║    ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗    
    ╚═╝      ╚═╝ ╚═════╝  ╚═════╝      ╚═╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    
    """
    slow_print(second_art, Fore.MAGENTA, 0.002)
    time.sleep(2)
    clear_screen()

    # Welcome message in Light Green
    welcome_message = Style.BRIGHT + "Prozzy karışık toola hoşgeldiniz"
    slow_print(welcome_message, Fore.LIGHTGREEN_EX, 0.05)
    time.sleep(2)
    clear_screen()

    while True:
        # Menu Header
        menu_header = """
        ██████╗ ██████╗  ██████╗ ███████╗███████╗██╗   ██╗
        ██╔══██╗██╔══██╗██╔═══██╗╚══███╔╝╚══███╔╝╚██╗ ██╔╝
        ██████╔╝██████╔╝██║   ██║  ███╔╝   ███╔╝  ╚████╔╝ 
        ██╔═══╝ ██╔══██╗██║   ██║ ███╔╝   ███╔╝    ╚██╔╝  
        ██║     ██║  ██║╚██████╔╝███████╗███████╗   ██║   
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
        """
        slow_print(menu_header, Fore.LIGHTMAGENTA_EX, 0.002)

        # Menu options
        print(Fore.LIGHTMAGENTA_EX + "1: ddos")
        print(Fore.LIGHTMAGENTA_EX + "2: sms boomber")
        print(Fore.LIGHTMAGENTA_EX + "3: eklenicek")
        choice = input(Fore.LIGHTGREEN_EX + "Seçiminizi girin: ")

        if choice == '1':
            os.system('python dosyalar/tool/prozzyddos.py')
        elif choice == '2':
            os.system('python dosyalar/tool/prozzysms.py')
        elif choice == '3':
            while True:
                slow_print("Toolumuza eklenmesini istediğiniz tüm özellikleri instagram veya whatsapp üzerinden detaylı şekilde iletin...", Fore.LIGHTGREEN_EX)
                print("1: Instagram")
                print("2: Whatsapp")
                print("3: Geri")
                sub_choice = input("Seçiminizi belirtin: ")
                if sub_choice == '1':
                    webbrowser.open("https://www.instagram.com/by.prozzy/")
                    break
                elif sub_choice == '2':
                    # Only open WhatsApp DM with the given phone number
                    whatsapp_url = "whatsapp://send?phone=+905310225234"
                    if platform.system() == "Windows":
                        os.system(f"start {whatsapp_url}")
                    else:
                        os.system(f"xdg-open \"{whatsapp_url}\"")
                    break
                elif sub_choice == '3':
                    break
                else:
                    print("Geçersiz seçim, tekrar deneyin...")
        else:
            print("Geçersiz seçim, programdan çıkılıyor...")
            break

if __name__ == "__main__":
    main()
