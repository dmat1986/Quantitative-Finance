import abc
import numpy as np
from market_data import MarketData

class Payoff(object):
	__metaclass__=abc.ABCMeta
	# @property
	# @abc.abstractmethod
	# def expiry(self):
	# 	pass

	# @expiry.setter
	# @abc.abstractmethod
	# def expiry(self, newExpiry):
	# 	self.__expiry = newExpiry
	# 	pass

	@abc.abstractmethod
	def payoff(self):
		pass

class VanillaPayoff(Payoff):
	def __init__(self, data, payoff):
		self.__spot = data.get_data()[0]
		self.__strike = data.get_data()[5]
		self.__payoff = payoff

	@property
	def spot(self):
		return self.__spot

	@spot.setter
	def spot(self, new_spot):
		self.__spot = new_spot

	@property
	def strike(self):
		return self.__strike

	@strike.setter
	def strike(self, new_strike):
		self.__strike = new_strike

	def payoff(self, spot, strike):
		return self.__payoff(spot, strike)

def call_payoff(spot, strike):
	return np.maximum(spot - strike, 0.0)

def put_payoff(spot, strike):
	return np.maximum(strike - spot, 0.0)