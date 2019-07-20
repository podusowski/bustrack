import requests


_URL = 'http://mpk.wroc.pl/position.php'


def fetch_positions(buses):
    '''Only buses for now!'''
    post_data = {'busList[bus][]': buses}
    r = requests.post(_URL, data=post_data)
    return r.json()


if __name__ == "__main__":
    p = fetch_positions([132, 107])
    print(p)
