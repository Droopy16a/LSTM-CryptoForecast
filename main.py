import argparse
from script import Crypto

def main():
    parser = argparse.ArgumentParser(description="Display cryptocurrency data")
    parser.add_argument('--crypto', type=str, required=True, help='Cryptocurrency symbol (e.g., BTC, ETH, PYUSD...)')
    parser.add_argument('--interval', type=str, help='Time interval (h, d, w, m, or y)')

    args = parser.parse_args()

    curr = args.crypto
    interval = args.interval

    c = Crypto()
    r = c.get_crypto(curr, interval)
    c.show()

if __name__ == "__main__":
    main()