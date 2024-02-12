import sys

from .args import parse_args
from confstore.client.client import start


def main():
    """
    CLI to run ConfigStore.
    """
    sockpath, stdout, verbose = parse_args(sys.argv[1:])
    start(sockpath, stdout, verbose)


if __name__ == "__main__":
    main()
