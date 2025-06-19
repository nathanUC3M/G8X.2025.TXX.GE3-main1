"""Logic for specific management of the Transfer json file"""
from uc3m_money.exception.account_management_exception import AccountManagementException
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.cfg.account_management_config import TRANSFERS_STORE_FILE

class TransfersJsonStore:
    """Transfers singleton"""
    class __TransfersJsonStore(JsonStore):
        """Class for dealing TransfersJsonStore"""
        _file_name = TRANSFERS_STORE_FILE

        def add_item(self, item):
            """Overrides the original method including the logic"""
            self.load_list_from_file()
            for old_transfer in self._data_list:
                if old_transfer == item.to_json():
                    raise AccountManagementException("Duplicated transfer in transfer list")
            super().add_item(item)

    instance = None
    def __new__(cls):
        if not TransfersJsonStore.instance:
            TransfersJsonStore.instance = TransfersJsonStore.__TransfersJsonStore()
        return TransfersJsonStore.instance

    def __getattr__(self, item):
        return getattr(TransfersJsonStore.instance, item)

    def __setattr__(self, key, value):
        return setattr(TransfersJsonStore.instance,key,value)
