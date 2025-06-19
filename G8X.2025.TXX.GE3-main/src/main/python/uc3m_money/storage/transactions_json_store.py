"""logic for dealing with the transcations file in json format"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.cfg.account_management_config import TRANSACTIONS_STORE_FILE

class TransactionsJsonStore:
    """transactions singleton"""
    class __TransactionsJsonStore(JsonStore):
        """Class for managing transactions' stores"""
        _file_name = TRANSACTIONS_STORE_FILE

        def find_all(self, key, value):
            """returns a list with the items that contains the
            pair key:value received """
            self.load_list_from_file()
            result_list = []
            for item in self._data_list:
                if item[key] == value:
                    result_list.append(item)
            return result_list

    instance = None
    def __new__(cls):
        if not TransactionsJsonStore.instance:
            TransactionsJsonStore.instance = TransactionsJsonStore.__TransactionsJsonStore()
        return TransactionsJsonStore.instance

    def __getattr__(self, item):
        return getattr(TransactionsJsonStore.instance, item)

    def __setattr__(self, key, value):
        return setattr(TransactionsJsonStore.instance,key,value)
