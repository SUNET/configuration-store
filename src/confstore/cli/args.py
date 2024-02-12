import argparse
import sys
from typing import Optional


def parse_args(cli_args: Optional[str] = ""):
    parser = argparse.ArgumentParser(description='Config Store CLI')
    parser.add_argument("-s", "--sockpath",
                        default="/usr/local/var/run/controller.sock",
                        help='Socket path for clixon-controller.')
    parser.add_argument("-o", "--stdout", action="store_true",
                        help="Logs on stdout instead of syslog.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Debug log.")
    args = parser.parse_args(cli_args)

    return (args.sockpath, args.stdout, args.verbose)


if __name__ == "__main__":
    parse_args(sys.argv[1:])
