import cloudscraper
import json
import os
from datetime import datetime
from widget import PlotWidget
import sys
from PyQt6.QtWidgets import QApplication

class Crypto:
    def __init__(self):
        self.get_crypto_list()

    def get_crypto_list(self):
        self.scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        url = 'https://price-api.crypto.com/meta/v1/all-tokens'

        # Check if crypto.json exists and is not empty
        if os.path.exists('crypto.json') and os.path.getsize('crypto.json') > 0:
            with open('crypto.json', 'r') as f:
                self.lst = json.load(f)
        else:
            r = self.scraper.get(url)
            self.lst = r.json()
            with open('crypto.json', 'w') as f:
                json.dump(self.lst, f)

    def get_crypto(self, C=None, timestamp="d"):
        self.timestamp = timestamp
        print(f"get_crypto: timestamp={timestamp}, self.timestamp={self.timestamp}")
        cryptoList = [(token["name"], token["symbol"]) for token in self.lst['data']]

        while C is None or C.lower() not in [crypto.lower() for crypto, _ in cryptoList] and C.lower() not in [symbol.lower() for _, symbol in cryptoList]:
            C = input("Enter the name of the cryptocurrency: ")

        for crypto, symbol in cryptoList:
            if C.lower() == crypto.lower() or C.lower() == symbol.lower():
                C = crypto
                break

        url = f'https://price-api.crypto.com/price/v2/{timestamp}/{C.lower().replace(" ", "-")}'
        r = self.scraper.get(url)
        self.C = C

        return r.json()
    
    def get_current_crypto(self, C=None):
        if C is None:
            C = self.C if hasattr(self, 'C') else "BTC"
        

    def show(self, color="#81ff4f"):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        crypto_data = self.get_crypto(self.C if hasattr(self, 'C') else None, timestamp=self.timestamp if hasattr(self, 'timestamp') else "d")
        window = PlotWidget(
            crypto_instance=self,
            currency=self.C if hasattr(self, 'C') else "BTC",
            timestamp=[datetime.fromtimestamp(i[0]) for i in crypto_data['prices']],
            data=[i[1] for i in crypto_data['prices']],
            color=color,
            tt=self.timestamp
        )
        window.show()
        sys.exit(app.exec())