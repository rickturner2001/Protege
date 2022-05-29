
from text_functions import center_text

def print_menu():
    print("General Help Menu:\n")
    print("Usage\t: -<general command> -<specific action> -<optional>\n")
    print("-db\t: Get access to the database (requires db commands follow-up)")
    print("-a\t: Do analysis (requires analysis commands follow-up)")

    print("\nAnalysis:\n")
    print("-s5\t: S5FI Analysis")
    print("-s5DF\t: Get 2 Years S5FI DataFrame (must be followd by file name)")
    print("-nsdma\t: NSDMA Analysis")
    print("\nMisc:\n")
    print("-v\t: Verbose Operation")