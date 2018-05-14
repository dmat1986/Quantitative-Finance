import abc

class MarketData(object):
	__metaclass__=abc.ABCMeta
	def __init__(self, spot, rate, volatility, dividend, expiry, strike):
		self.__rate = rate
		self.__spot = spot
		self.__volatility = volatility
		self.__dividend = dividend
		self.__expiry = expiry
		self.__strike = strike

	@property
	def rate(self):
		return self.__rate

	@rate.setter
	def rate(self, new_rate):
		self.__rate = new_rate

	@property
	def spot(self):
		return self.__spot

	@spot.setter
	def spot(self, new_spot):
		self.__spot = new_spot

	@property
	def volatility(self):
		return self.__volatility

	@volatility.setter
	def volatility(self, new_volatility):
		self.__volatility = new_volatility

	@property
	def dividend(self):
		return self.__dividend

	@dividend.setter
	def dividend(self, new_dividend):
		self.__dividend = new_dividend

	@property
	def expiry(self):
		return self.__expiry

	@expiry.setter
	def expiry(self, new_expiry):
		self.__expiry = new_expiry

	@property
	def strike(self):
		return self.__strike

	@strike.setter
	def strike(self, new_strike):
		self.__strike = new_strike

	def get_data(self):
		return (self.__spot, self.__rate, self.__volatility, 
			self.__dividend, self.__expiry, self.__strike)