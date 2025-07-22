import json
import pandas as pd
from pprint import pprint


class ExtractData:
    """
    this class is a used as helper class to extract data from google sheet
    """

    def __init__(self, path: str):
        self.path = path
        store_data = json.load(open(self.path))
        # temp_id = 0
        # for store in store_data:
        #     store["id"] = temp_id+1
        #     temp_id +=1
        self.data = store_data

    def grocery_data(self):
        resp = []
        temp_id = 0
        for store in self.data:
            store["store_id"] = temp_id + 1
            temp_id += 1
            print(store["dataSource"])
            resp.append(self.extract_data_from_google_sheet(store.copy()))
        print()
        print("Stores Data:")
        pprint(resp)
        return resp.copy()

    def extract_data_from_google_sheet(self, store_data: dict) -> dict:
        """
        This function Extract data from google sheet
        (url) -> dict
        """
        url = store_data["dataSource"]
        url = f"{url[:url.rfind('/')]}/export?format=csv"
        sheets = pd.read_csv(url)
        data = sheets.to_dict("index")
        temp = 0
        for _, val in data.items():
            temp += 1
            val["id"] = temp
            val.update(store_data)
        return list(data.values()).copy()


if __name__ == "__main__":
    ExtractData("data/stores.json").grocery_data()
