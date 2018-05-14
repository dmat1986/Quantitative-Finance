import abc
import enum

class Option(object):
	__metaclass__=abc.ABCMeta
	def __init__(self, option, engine, data):
		self.option = option
		self.engine = engine
		self.data = data

	def price(self):
		return self.engine.calculate(self.option, self.data)

	def greek(self):
		return self.engine.getGreeks(self.option, self.data, self.engine.pricer)