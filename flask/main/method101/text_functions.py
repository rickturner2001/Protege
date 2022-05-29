import os

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

# Text Color
def succesfull_action(message):
    print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}")
def failed_action(message):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")
def warning_message(message):
    print(f"{bcolors.WARNING}{message}{bcolors.ENDC}")
def cyan_message(message):
    print(f"{bcolors.OKCYAN}{message}{bcolors.ENDC}")

# Text alignment
def center_text(message):
    print(f"{message}".center(os.get_terminal_size().columns))

def banner():
    print("=" * 80)