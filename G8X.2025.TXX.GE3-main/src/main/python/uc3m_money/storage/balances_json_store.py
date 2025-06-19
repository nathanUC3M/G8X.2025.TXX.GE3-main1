"""Manages the balnces json store"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.cfg.account_management_config import BALANCES_STORE_FILE

class BalancesJsonStore:
    """balances singleton"""
    class __BalancesJsonStore(JsonStore):
        """class for managing Balances' stores"""
        _file_name = BALANCES_STORE_FILE

    instance = None
    def __new__(cls):
        if not BalancesJsonStore.instance:
            BalancesJsonStore.instance = BalancesJsonStore.__BalancesJsonStore()
        return BalancesJsonStore.instance

    def __getattr__(self, item):
        return getattr(BalancesJsonStore.instance, item)

    def __setattr__(self, key, value):
        return setattr(BalancesJsonStore.instance,key,value)
