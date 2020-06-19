import transmissionrpc
from transmissionrpc import TransmissionError
import config
from datetime import datetime, timedelta
import sys

HOST = config.HOST
PORT = config.PORT
USER = config.USER
PASSWORD = config.PASSWORD
TC = transmissionrpc.Client(HOST, port=PORT, user=USER, password=PASSWORD, timeout="10")


def main(days=90):
    """
    Remove all torrents that are older than number of "days" from today
    :return:
    """
    try:
        torrents = get_torrent_list(TC)
        old = _time_based_list(torrents, int(days))
        remove_torrents(old)
    except TransmissionError as e:
        print(e)


def remove_torrents(l):
    """
    Given  a list of torrents, remove each one
    :param l:
    :return:
    """
    print("About to remove "+str(len(l))+" torrents")
    for torrent in l:
        _remove_single_torrent(torrent)


def _remove_single_torrent(t):
    """
    Remove a single torrent
    :param t: torrent object
    :return: None
    """
    try:
        TC.remove_torrent(t.id, delete_data=True, timeout=None)
        print("removing :"+str(t.id))
    except ValueError as e:
        print("Error: "+str(t.id)+" not removed."+e)


def get_torrent_list(session):
    """
    Give a session, return the list of torrents on the server
    :param session:
    :return: list
    """
    try:
        torrents = TC.get_torrents()
        return torrents
    except KeyError as e:
        pass


def _time_based_list(l, delta=30):
    """
    Given a list of torrent objects return a list of the torrents that are older than "delta" days from now()
    :param l: list
    :param delta: int
    :return: list
    """
    old = []
    for torrent in l:
        torrent_complete = torrent.date_done
        if torrent_complete + timedelta(delta) < datetime.now():
            old.append(torrent)
    return old


if __name__ == '__main__':
    if sys.argv[1]:
        main(sys.argv[1])
    else:
        main()

