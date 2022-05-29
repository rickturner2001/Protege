import sys
from text_functions import *
from menus import print_menu
from cli_commands import analysis_functions
from sefi100 import get_sefi100
from ma_difference import get_nsdma_signals



# No flags were passed 
if len(sys.argv) == 1:
    failed_action(f"Unsuccessful action. try: {sys.argv[0]} -h or --help (help and commands)")
else:
    try:
        # Only one flag was passed. Must be -h or --help
        banner()
        center_text("Simple Stock Screener\n")
        if len(sys.argv) == 2:
            if sys.argv[1] == '-h' or sys.argv[1] == '--help':
                print_menu()
            else:
                failed_action(f"Expected multiple arguments but was given '{sys.argv[1]}'. Try -h or --help")
                sys.exit()
                
        else:
            # Multiple parameters were passed 
            # First parameter check
            if sys.argv[1] == '-a':
                # Second parameter check
                if sys.argv[2] == '-s5': 
                    analysis_functions(sys.argv, get_sefi100, "Succesfully started S5FI analysis")
                if sys.argv[2] == '-nsdma':
                    analysis_functions(sys.argv, get_nsdma_signals, "Succesfully started NSDMA analysis")

                if sys.argv[2] == '-s5DF':
                    analysis_functions(sys.argv, get_sefi100, "Succesfully started S5FI DataFrame", save_output=True)
        print()   
        banner()
    except KeyboardInterrupt:
        warning_message("\nClosing process....")
        sys.exit()