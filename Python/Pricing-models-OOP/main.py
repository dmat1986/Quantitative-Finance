from financial_instrument import Option
from market_data import MarketData
from payoff import VanillaPayoff, call_payoff, put_payoff
from pricing_engine import (MonteCarloPricingEngine, 
	Naive_Monte_Carlo_Pricer, BlackScholesPricingEngine, 
	BlackScholesPricer, BinomialPricingEngine, BinomialPricer, Greeks)

strike = 40.0

spot = 41.0
rate = 0.08
volatility = 0.30
dividend = 0.0
expiry = 0.25

replications = 1000000
time_steps = 1000000

binomial_steps = 300

pricer = BinomialPricer
optionType = "put"
optionPayoff = put_payoff

engine = BinomialPricingEngine(binomial_steps, pricer, Greeks)
the_data = MarketData(spot, rate, volatility, dividend, expiry, strike)
the_payoff = VanillaPayoff(the_data, optionPayoff)
option = Option(the_payoff, engine, the_data)
price = option.price()
greeksVec = option.greek()

print(price)
print(greeksVec)