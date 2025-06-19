"""Class for managing the deposits json store"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.cfg.account_management_config import DEPOSITS_STORE_FILE

class DepositsJsonStore:
    """desposits singleton"""
    class __DepositsJsonStore(JsonStore):
        """class for managing deposits' stores"""
        _file_name = DEPOSITS_STORE_FILE

    instance = None
    def __new__(cls):
        if not DepositsJsonStore.instance:
            DepositsJsonStore.instance = DepositsJsonStore.__DepositsJsonStore()
        return DepositsJsonStore.instance

    def __getattr__(self, item):
        return getattr(DepositsJsonStore.instance, item)

    def __setattr__(self, key, value):
        return setattr(DepositsJsonStore.instance,key,value)
