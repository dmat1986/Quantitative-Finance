#include<cmath>
#include<cstdlib>
double random_uniform_0_1()
{
  return double(rand())/double(RAND_MAX);
}
double random_normal()
{
  double U1, U2, V1, V2;
  double S=2;
  while (S >= 1)
    {
      U1 = random_uniform_0_1();
      U2 = random_uniform_0_1();
      V1 = 2.0 * U1 - 1.0;
      V2 = 2.0 * U2 - 1.0;
      S = pow(V1, 2) + pow(V2, 2);
    }
  double X1 = V1 * sqrt((-2.0 * log(S)) / S);
  return X1;
}

#include<string>
using namespace std;
class AsianOption
{
public:
  AsianOption();
  AsianOption(const double& _S0, const double& _K,
	      const double& _r, const int& T, const double& vol,
	      const string& type);
  AsianOption(const AsianOption& asianOpt2);
  virtual ~AsianOption();

  AsianOption& operator = (const AsianOption& asianOpt2);

  double NPV() const; //contains option price

  double MonteCarloSim() const; //calculates option price

private:
  double S0; //underlying stock price
  double K; //strike price
  double r; //risk-neutral interest rate;
  int T; //time to maturity (in years)
  double sigma; //volatility
  string optType; //option type (call, put)
};

 
#include<iostream>
#include<math.h>
#include<vector>
#include<numeric>
//#include<cstdlib>
#include<string>
AsianOption::AsianOption()
{
  S0 = 50.0;
  K = 50.0;
  r = 0.04;
  T = 2;
  sigma = 0.4;
  optType = "call";

}
AsianOption::AsianOption(const double& _S0, const double& _K,
			 const double& _r, const int& _T, const double& vol,
			 const string& type)
  : S0(_S0), K(_K), r(_r), T(_T), sigma(vol), optType(type)
{
} 

AsianOption::AsianOption(const AsianOption& aOpt2)
{
  S0 = aOpt2.S0;
  K = aOpt2.K;
  r = aOpt2.r;
  T = aOpt2.T;
  sigma = aOpt2.sigma;
  optType = aOpt2.optType;
}
AsianOption::~AsianOption()
{
}
AsianOption& AsianOption::operator = (const AsianOption& asianOpt2)
{
  if (this == &asianOpt2)
    return *this;

  S0 = asianOpt2.S0;
  K = asianOpt2.K;
  r = asianOpt2.r;
  T = asianOpt2.T;
  sigma = asianOpt2.sigma;
  optType = asianOpt2.optType;

  return *this;
}
double AsianOption::MonteCarloSim() const
{
  const int& days = T * 250;
  const double& d_t = 1.0/250.0;
  const int& noSims = 100000;
  double sum_cPayoff = 0.0;
  double sum_pPayoff = 0.0;

  vector<double> prices(days);

  double S_t;
  double left, right;

  left = (r - pow(sigma,2)/2)*d_t;
  right = sigma * sqrt(d_t);

  srand((unsigned)time(0));

  for(int j = 0; j < noSims; j++)
    {
      S_t = S0;
      for (int i = 0; i < days; i++)
	{
	  prices[i] = S_t;
	  S_t = S_t * exp(left + right * random_normal());
	}
      double sum = accumulate(prices.begin(),prices.end(),0.0);
      double avgPrice = sum / prices.size();
      double cPayoff = max(0.0,avgPrice-K);
      sum_cPayoff = sum_cPayoff + cPayoff;
      double pPayoff = max(0.0,K-avgPrice);
      sum_pPayoff = sum_pPayoff + pPayoff;
    }

  double avg_cPayoff = sum_cPayoff/noSims;
  double avg_pPayoff = sum_pPayoff/noSims;

  double callPrice = exp(-r*T)*(avg_cPayoff);

  double putPrice = exp(-r*T)*(avg_pPayoff);
  if(optType == "call" || optType == "Call")
    return callPrice;
  else if (optType == "put" || optType == "Put")
    return putPrice;
  else
    cout << "Invalid option type." << endl;
  return 0;
}
double AsianOption::NPV() const
{
  return MonteCarloSim();
} 

using namespace std;

int main( )
{

  AsianOption asOpt;

  std::cout << asOpt.NPV() << endl;

  system("pause");
  return 0;
}

