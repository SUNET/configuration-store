from socket import socket
import time

from clixon.helpers import get_devices
from clixon.netconf import rpc_config_get, rpc_subscription_create
from clixon.parser import parse_string
from clixon.sock import read, send, create_socket

from confstore.util.log import get_logger

logger = ""


def handle_controller_transaction(sock: socket, data):
    """
    Called on controller transaction
    """
    print("NOTIFICATION\n{}\n".format(data.dumps()))
    logger.debug("Received notification transaction")

    get_config_req = rpc_config_get(source="running")
    send(sock, get_config_req)


def handle_reply(data):
    """
    :param data: xml tree data node
    """
    print("REPLY\n{}\n".format(data.dumps()))
    logger.debug("Received rpc reply")
    for dev in get_devices(data):
        print(dev)
        print(dev.dumps())
        print()


def read_loop(sock: socket) -> None:
    """
    Socket read loop.
    :param socket: IPC socket
    """

    logger.info("Listening...")

    while True:
        try:
            data = read(sock)
            data_parsed = parse_string(data)
        except Exception as ex:
            logger.error(f"Read loop got an exception: {ex}")
            print(f"error {ex}")
            time.sleep(3)
            break

        if _is_rpc_reply(data):
            handle_reply(data_parsed.rpc_reply.data)
        elif _is_controller_transaction(data):
            handle_controller_transaction(sock, data_parsed)


def _is_rpc_reply(msg: str):
    return "<rpc-reply" in msg and "<devices" in msg


def _is_controller_transaction(msg: str):
    return "<notification" in msg and "<controller-transaction" in msg


def start(sockpath: str, stdout: bool, verbose: bool):
    """
    Create socket at sockpath, subscribe to events and start read loop.

    :param sockpath: Socket path
    :param stdout: Log to stdout
    :param verbose: Verbose logging
    """
    global logger  # TODO: consider not using global
    logger = get_logger(stdout, verbose)

    while True:
        logger.debug("Creating socket and subscribe for notification")

        try:
            sock = create_socket(sockpath)
        except Exception as ex:
            logger.error(f"Could not connect to socket: {ex}")
            time.sleep(3)
            continue

        try:
            logger.info("Subscribe to controller-transaction")
            enable_transaction_notify = rpc_subscription_create(
                "controller-transaction")
            send(sock, enable_transaction_notify)
            response = read(sock)
            logger.info(f"enabled subscription: {response}")
        except Exception as ex:
            logger.error(str(ex))
            return

        read_loop(sock)


if __name__ == "__main__":
    sockpath = "/usr/local/var/run/controller.sock"
    start(sockpath, True, True)
