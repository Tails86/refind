import sys
from .find import main as find_main

def main():
    ''' Find main using arguments from sys.argv '''
    cliargs = sys.argv[1:]
    try:
        return find_main(cliargs)
    except Exception as e:
        if '-verbose' not in cliargs:
            # Format the exception into a less verbose output
            print('{}: {}'.format(type(e).__name__, str(e)), file=sys.stderr)
            return 1
        else:
            # Allow Python repl to format the exception to output
            raise e

# Execute above
sys.exit(main())
