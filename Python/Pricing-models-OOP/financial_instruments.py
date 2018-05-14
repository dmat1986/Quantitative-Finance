class Asset():
	def __init__(self, spot_price):
		self.spot_price = spot_price

class Equity(Asset):
	def __init__(self, spot_price, mean, volatility, dividend_yield):
		Asset.__init__(self, spot_price)
		self.mean = mean
		self.volatility = volatility
		self.dividend_yield = dividend_yield

class Bond(Asset):
	def __init__(self, spot_price, coupon_rate, num_coupons, 
		discount_rate, time_to_redemption):
		Asset.__init__(self, spot_price)
		self.coupon_rate = coupon_rate
		self.num_coupons = num_coupons
		self.discount_rate = discount_rate
		self.time_to_redemption = time_to_redemption

class Derivative(Asset):
	def __init__(self, spot_price, risk_free_rate, time_to_maturity):
		Asset.__init__(self, spot_price)
		self.risk_free_rate = risk_free_rate
		self.time_to_maturity = time_to_maturity

class Option(Derivative):
	def __init__(self, spot_price, strike_price, risk_free_rate, 
		time_to_maturity, optType):
		Derivative.__init__(self, spot_price, risk_free_rate, 
			time_to_maturity)
		self.strike_price = strike_price
		self.optType = optType

class Forward(Derivative):
	def __init__(self, spot_price, risk_free_rate, 
		time_to_maturity):
		Derivative.__init__(self, spot_price, risk_free_rate, 
			time_to_maturity)

class Futures(Derivative):
	def __init__(self, spot_price, risk_free_rate, 
		time_to_maturity):
		Derivative.__init__(self, spot_price, risk_free_rate, 
			time_to_maturity)