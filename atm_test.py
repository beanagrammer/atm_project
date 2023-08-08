from atm import Bank
import unittest
import asyncio
from contextlib import suppress

# (Assuming you've pasted the previous code for Account, ATMController, and Bank classes here)

class TestATMSystem(unittest.TestCase):

	def setUp(self):
		print("\n" + "-"*75)
		print(f"Running test: {self.id().split('.')[-1]}")
		print("-"*75 + "\n")
		self.bank = Bank("CIBC")
		self.bank.add_account("12341231", 1000, "1234")

	def test_correct_pin(self):
		async def run_test():
			print("Inserting card...")
			self.bank.atm_controller.insert_card("12341231")
			print("Entering correct PIN...")
			is_authenticated = await self.bank.atm_controller.enter_pin("1234")
			self.assertTrue(is_authenticated)
		asyncio.run(run_test())

	def test_incorrect_pin(self):
		async def run_test():
			print("Inserting card...")
			self.bank.atm_controller.insert_card("12341231")
			print("Entering incorrect PIN...")
			is_authenticated = await self.bank.atm_controller.enter_pin("9999")
			self.assertFalse(is_authenticated)
		asyncio.run(run_test())

	def test_balance_check(self):
		print("Inserting card...")
		self.bank.atm_controller.insert_card("12341231")
		with suppress(Exception):
			print("Entering PIN...")
			asyncio.run(self.bank.atm_controller.enter_pin("1234"))
		print("Checking balance...")
		balance = self.bank.atm_controller.display_balance()
		self.assertEqual(balance, 1000)

	def test_withdraw_more_than_balance(self):
		print("Inserting card...")
		self.bank.atm_controller.insert_card("12341231")
		with suppress(Exception):
			print("Entering PIN...")
			asyncio.run(self.bank.atm_controller.enter_pin("1234"))
		print("Attempting to withdraw more than balance...")
		with self.assertRaises(ValueError):
			self.bank.atm_controller.withdraw(1500)

	def test_deposit_and_withdraw(self):
		print("Inserting card...")
		self.bank.atm_controller.insert_card("12341231")
		with suppress(Exception):
			print("Entering PIN...")
			asyncio.run(self.bank.atm_controller.enter_pin("1234"))
		print("Depositing money...")
		self.bank.atm_controller.deposit(300)
		balance_after_deposit = self.bank.atm_controller.display_balance()
		self.assertEqual(balance_after_deposit, 1300)
		print("Withdrawing money...")
		self.bank.atm_controller.withdraw(200)
		balance_after_withdraw = self.bank.atm_controller.display_balance()
		self.assertEqual(balance_after_withdraw, 1100)

	def test_eject_card(self):
		print("Inserting card...")
		self.bank.atm_controller.insert_card("12341231")
		with suppress(Exception):
			print("Entering PIN...")
			asyncio.run(self.bank.atm_controller.enter_pin("1234"))
		print("Ejecting card...")
		self.bank.atm_controller.eject_card()
		print("Attempting operation post card ejection...")
		with self.assertRaises(PermissionError):
			self.bank.atm_controller.display_balance()



if __name__ == "__main__":
    unittest.main()
