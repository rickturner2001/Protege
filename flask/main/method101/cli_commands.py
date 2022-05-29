import sys
from pathlib import Path

CURRENT_DIR = str(Path(__file__).resolve().parent.parent / 'utilities')
from text_functions import succesfull_action, failed_action


def save(save_output, filename, result):
    if save_output and not filename:
        failed_action("You need to provide a file name")
        sys.exit()
    elif save_output and filename:
        if not isinstance(result, list):
            with open(f"{filename}.txt", 'w') as f:
                f.write(str(result))
        else:
            with open(f"{filename}.txt", 'w') as f:
                for row in result:
                    f.write(str(row))


def analysis_functions(sys_args, func, starting_msg, save_output=False, filename=None):
    if len(sys_args) == 5:  # Must be a save file:
        if sys_args[4][0] == '-':
            failed_action(f"Optional parameter {sys_args[4]} wasn't expected")
            sys.exit()
        else:
            filename = sys_args[4]
            print(sys_args)
            print("FILENAME ", filename)
            # TODO check if sys_args[3] is -v
            result = func(verbose=True, df_return=True)
            if save_output: save(save_output, filename, result)

        if save_output: save(save_output, filename, result)
    elif len(sys_args) == 4:
        if sys_args[3] == "-v":
            succesfull_action(f"{starting_msg} (verbose)")
            result = func(verbose=True, df_return=True)
            if save_output:
                save(save_output, filename, result)

        else:
            if sys_args[3][0] == '-':
                failed_action(f"Optional parameter {sys_args[3]} wasn't expected")
                sys.exit()
            else:
                filename = sys_args[3]
                result = func(verbose=True, df_return=True)
                if save_output:
                    save(save_output, filename, result)

    else:
        succesfull_action(f"{starting_msg}")
        result = func(df_return=True)
        print("save", save_output, "filename", filename)
        if save_output:
            save(save_output, filename, result)
