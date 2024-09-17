# solo_server/cli.py

import argparse
from solo_server.commands import init

def main():
    parser = argparse.ArgumentParser(description='Solo Server CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Init command
    subparsers.add_parser('init', help='Initialize a new project')

    args = parser.parse_args()

    if args.command == 'init':
        init.handle_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
