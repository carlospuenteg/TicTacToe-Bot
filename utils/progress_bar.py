from colorama import Fore, init; init()

def progress_bar(percent, text="", bar_len=30):
    SYMBOL = "━"
    done = round(percent*bar_len)
    left = bar_len - done

    print(f"   {Fore.GREEN}{SYMBOL*done}{Fore.RESET}{SYMBOL*left} {f'[{round(percent*100,2)}%]'.ljust(8)} {Fore.MAGENTA}{text}{Fore.RESET}", end='\r')

    if percent == 1: print("✅")