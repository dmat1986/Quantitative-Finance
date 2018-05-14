import abc
import numpy as np
import scipy.stats as sp
from scipy.special import comb
from market_data import MarketData
from mathematics import round_up_to_odd

class PricingEngine(object):
	__metaclass__=abc.ABCMeta
	def calculate(self):
		pass

class BinomialPricingEngine(PricingEngine):
	def __init__(self, steps, pricer, greeks):
	#def __init__(self, steps, pricer, greeks):
		self.__steps = steps
		self.pricer = pricer
		self.__greeks = greeks

	@property
	def steps(self):
		return self.__steps

	@steps.setter
	def steps(self, new_steps):
		self.__steps = new_steps

	def calculate(self, option, data):
		return self.pricer(self, option, data)

	def getGreeks(self, option, data, pricer):
		return self.__greeks(self, option, data, pricer)

def BinomialPricer(engine, option, data):
	(spot, rate, volatility, dividend, expiry, strike) = data.get_data()
	n = engine.steps
	#n = round_up_to_odd(n)
	dt = expiry / n
	#u = np.exp(volatility * np.sqrt(dt))
	#d = 1.0 / u
	#p = (np.exp((rate-dividend)*dt)-d) / (u-d)
	u = np.exp((rate-dividend-0.5*volatility*volatility)*dt+volatility*np.sqrt(dt))
	d = np.exp((rate-dividend-0.5*volatility*volatility)*dt-volatility*np.sqrt(dt))
	#Df = np.exp(-rate*expiry)
	drift = np.exp(rate*dt)
	q = (drift-d)/(u-d)
	
	stkval = np.zeros((n+1,n+1))
	optval = np.zeros((n+1,n+1))
	stkval[0,0] = spot
	for i in range(1,n+1):
		stkval[i,0] = stkval[i-1,0]*u
		for j in range(1, i+1):
			stkval[i,j] = stkval[i-1,j-1]*d

	for j in range(n+1):
		optval[n,j] = option.payoff(stkval[n,j], strike)
	
	for i in range(n-1,-1,-1):
		for j in range(i+1):
			optval[i,j] = (q*optval[i+1,j]+(1.0-q)*optval[i+1,j+1])/drift

	price = optval[0,0]
	# delta = (optval[1,1]-optval[1,0])/(spot*u-spot*d)
	# topleft = (optval[2,2]-optval[2,1])/(spot*u*u-spot)
	# topright = (optval[2,1]-optval[2,0])/(spot-spot*d*d)
	# bottom = 0.5*(spot*u*u-spot*d*d)
	# gamma = (topleft-topright)/bottom
	# theta = (optval[2,1]-optval[0,0])/(2.0*dt*365)

	return price

	# sum_ = 0.0

	# for j in range(n):
	# 	Si = spot * u**j * d**(n-j)
	# 	sum_ += comb(n,j)* p**j * (1-p)**(n-j)*option.payoff(Si, strike)

	# price = Df*sum_

	# return price

class BlackScholesPricingEngine(PricingEngine):
	def __init__(self, optType, pricer, greeks):
		self.__optType = optType
		self.pricer = pricer
		self.__greeks = greeks

	@property
	def optType(self):
		return self.__optType

	@optType.setter
	def optType(self, new_optType):
		self.__optType = new_optType

	def calculate(self, option, data):
		return self.pricer(self, option, data)

	def getGreeks(self, option, data, pricer):
		return self.__greeks(self, option, data, pricer)

def BlackScholesPricer(engine, option, data):
	(spot, rate, volatility, q, expiry, strike) = data.get_data()
	opt_type = engine.optType
	discount_rate = np.exp(-rate * expiry)
	dqr = np.exp(-q*expiry)
	
	d1 = (1.0/(volatility*np.sqrt(expiry)))*(np.log(spot/strike)+
		((rate-q)+volatility*volatility*0.5)*expiry)
	d2 = d1 - volatility*np.sqrt(expiry)

	def N(x):
		return sp.norm.cdf(x)

	if (opt_type == "call") or (opt_type == "Call"):
		price = N(d1)*spot*dqr-N(d2)*strike*discount_rate
	elif (opt_type == "put") or (opt_type == "Put"):
		price = N(-d2)*strike*discount_rate-N(-d1)*spot*dqr

	return price


class MonteCarloPricingEngine(PricingEngine):
	def __init__(self, replications, time_steps, pricer):
		self.__replications = replications
		self.__time_steps = time_steps
		self.pricer = pricer
		#self.__greeks = greeks

	@property
	def replications(self):
		return self.__replications

	@replications.setter
	def replications(self, new_replications):
		self.__replications = new_replications

	@property
	def time_steps(self):
		return self.__time_steps

	@time_steps.setter
	def time_steps(self, new_time_steps):
		self.__time_steps = new_time_steps

	def calculate(self, option, data):
		return self.pricer(self, option, data)

	# def getGreeks(self, option, data, pricer):
	# 	return self.__greeks(self, option, data, pricer)

def Naive_Monte_Carlo_Pricer(engine, option, data):
	(S, r, V, q, T, strike) = data.get_data()
	time_steps = engine.time_steps
	replications = engine.replications
	discount_rate = np.exp(-r * T)
	delta_t = T / time_steps
	z = np.random.normal(size = time_steps)

	nudt = ((r-q)-0.5*V*V)*T
	sidt = V*np.sqrt(T)

	S_t = np.zeros((replications, ))
	payoff_t = 0.0
	for i in range(replications):
		S_t = S * np.exp(nudt + sidt * z[i])
		payoff_t += option.payoff(S_t, strike)

	payoff_t /= replications
	price = discount_rate * payoff_t

	return price

def Greeks(engine, option, data, pricer):
	alpha = 0.0001 
	(spot, rate, volatility, dividend, expiry, strike) = data.get_data()
	discount = np.exp(-rate*expiry)
	delta = (pricer(engine, option, 
		MarketData(spot+alpha, rate, volatility, dividend, 
			expiry, strike)) - 
		pricer(engine, option, MarketData(spot, rate, 
		volatility, dividend, expiry, strike))) / alpha
	gamma = ((pricer(engine, option, 
		MarketData(spot+alpha, rate, volatility, dividend, 
			expiry, strike)) -2.0*
		pricer(engine, option, MarketData(spot, rate, 
		volatility, dividend, expiry, strike))) + pricer(engine, option, 
		MarketData(spot-alpha, rate, volatility, 
			dividend, expiry, strike)))/(alpha*alpha)
	rho = (pricer(engine, option, 
		MarketData(spot, rate+alpha, volatility, dividend, 
			expiry, strike)) - 
		pricer(engine, option, MarketData(spot, rate, 
		volatility, dividend, expiry, strike))) / alpha
	vega = (pricer(engine, option, 
		MarketData(spot, rate, volatility+alpha, dividend, 
			expiry, strike)) - 
		pricer(engine, option, MarketData(spot, rate, 
		volatility, dividend, expiry, strike))) / alpha	
	theta = (pricer(engine, option, 
		MarketData(spot, rate, volatility, dividend, 
			expiry-(1.0/365.0), strike)) - 
		pricer(engine, option, MarketData(spot, rate, 
		volatility, dividend, expiry, strike)))

	return (delta, gamma, rho/100.0, vega/100.0, theta)