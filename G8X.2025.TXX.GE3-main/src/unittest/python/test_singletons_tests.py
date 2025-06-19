"""Singleton test cases"""
from unittest import TestCase
from uc3m_money import (AccountManager,
                        TransfersJsonStore,
                        TransactionsJsonStore,
                        BalancesJsonStore,
                        DepositsJsonStore)

class TestSingletons(TestCase):
    """Class for testing the singletons"""
    def test_account_manager_singleton(self):
        """singleton account manager"""
        ac1 = AccountManager()
        ac2 = AccountManager()
        ac3 = AccountManager()
        self.assertEqual(ac1,ac2)
        self.assertEqual(ac2,ac3)
        self.assertEqual(ac1,ac3)

    def test_transactions_store(self):
        """transactions json store singleton"""
        tjs1 = TransactionsJsonStore()
        tjs2 = TransactionsJsonStore()
        tjs3 = TransactionsJsonStore()
        self.assertEqual(tjs1, tjs2)
        self.assertEqual(tjs2, tjs3)
        self.assertEqual(tjs3, tjs1)

    def test_transfer_store(self):
        """transfer json store singleton"""
        tjs1 = TransfersJsonStore()
        tjs2 = TransfersJsonStore()
        tjs3 = TransfersJsonStore()
        self.assertEqual(tjs1, tjs2)
        self.assertEqual(tjs2, tjs3)
        self.assertEqual(tjs3, tjs1)

    def test_balances_store(self):
        """balances json store singleton"""
        bjs1 = BalancesJsonStore()
        bjs2 = BalancesJsonStore()
        bjs3 = BalancesJsonStore()
        self.assertEqual(bjs1, bjs2)
        self.assertEqual(bjs2, bjs3)
        self.assertEqual(bjs3, bjs1)

    def test_deposits_store(self):
        """desposits json store singleton"""
        djs1 = DepositsJsonStore()
        djs2 = DepositsJsonStore()
        djs3 = DepositsJsonStore()
        self.assertEqual(djs1, djs2)
        self.assertEqual(djs2, djs3)
        self.assertEqual(djs3, djs1)