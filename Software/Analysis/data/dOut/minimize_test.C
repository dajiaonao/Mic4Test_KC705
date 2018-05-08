#include "Minuit2/Minuit2Minimizer.h"
#include "Math/Functor.h"
#include <vector>
#include <utility>
#include <fstream>
#include <cmath>

double RosenBrock(const double *xx )
{
  const Double_t x = xx[0];
  const Double_t y = xx[1];
  const Double_t tmp1 = y-x*x;
  const Double_t tmp2 = 1-x;
  return 100*tmp1*tmp1+tmp2*tmp2;
}


std::vector< std::pair<float, int> > data1;

void get_data0(){
  data1.push_back(std::make_pair(0.1,0));
  data1.push_back(std::make_pair(0.2,0));
  data1.push_back(std::make_pair(0.25,0));
//   data1.push_back(std::make_pair(0.25001,1));
//   data1.push_back(std::make_pair(0.25002,0));
//   data1.push_back(std::make_pair(0.26001,1));
//   data1.push_back(std::make_pair(0.26002,0));
  data1.push_back(std::make_pair(0.27,1));
  data1.push_back(std::make_pair(0.3,1));
  data1.push_back(std::make_pair(0.4,1));
  data1.push_back(std::make_pair(0.5,1));
  data1.push_back(std::make_pair(0.6,1));
}


void get_data(){
  data1.reserve(700);
  int id, v;
  float vL, vH, x;

  std::ifstream fin("ENC_0507_Chip5Col12_scan_normal_try1.dat");
  while(fin){
    fin >> id >> vL >> vH >> v;
    data1.push_back(std::make_pair(vH-vL, v));
   }
//   std::cout << vL << " " << vH  << " " << v << std::endl;
//   std::cout << data1.size() << std::endl;
//   std::cout << data1[0].first << "->" << data1[data1.size()-1].first << std::endl;

  return;
}

const double sqrt2 = TMath::Sqrt(2);

double intL(const double *xx){
  // xx[0] is mean and xx[1] is width, xx[2] is the conditional observable, xx[3] is the meansurement
  double val = 1.;
  int j = 0;
  for(auto a: data1){
//     if(a.first<0.13 or a.first>0.15) continue;

    double P = 0.5*(1.+TMath::Erf((a.first-xx[0])/(sqrt2*xx[1])));
    val *= a.second?P:(1-P);
//     std::cout << a.first << " " << a.second << " -> " << val << " " << P << std::endl;
    j+=1;
//     if(j>10) break;
   }

  return -2*log(val);
}


int NumericalMinimization()
{
   // Choose method upon creation between:
   // kMigrad, kSimplex, kCombined, 
   // kScan, kFumili
   ROOT::Minuit2::Minuit2Minimizer min ( ROOT::Minuit2::kMigrad );
 
   min.SetMaxFunctionCalls(1000000);
   min.SetMaxIterations(100000);
   min.SetTolerance(0.001);
 
//    ROOT::Math::Functor f(&RosenBrock,2); 
   ROOT::Math::Functor f(&intL,2); 
   double step[2] = {0.0001,0.0001};
   double variable[2] = {0.5,0.3};
 
   min.SetFunction(f);
 
   // Set the free variables to be minimized!
   min.SetVariable(0,"mu",variable[0], step[0]);
   min.SetVariable(1,"sigma",variable[1], step[1]);

   min.SetVariableLimits(0, 0.05, 0.8);
   min.SetVariableLimits(1, 0.0005, 0.2);
 
   min.Minimize(); 
 
   const double *xs = min.X();
   cout << "Minimum: f(" << xs[0] << "," << xs[1] << "): " 
        << intL(xs) << endl;
//         << RosenBrock(xs) << endl;

   double err1, err2;
   min.GetMinosError(0, err1, err2);
   cout << "mean error:" << err1 << " " << err2 << std::endl;
   min.GetMinosError(1, err1, err2);
   cout << "width error:" << err1 << " " << err2 << std::endl;


   return 0;
}

int minimize_test(){
//   get_data();
  get_data0();
  return NumericalMinimization(); 

  double par[] = {0.17,0.005};
  std::cout << "the value " << intL(par) << std::endl;;
// 
//   par[0] = 0.136;
//   par[1] = 0.007;
//   std::cout << intL(par) << std::endl;
  return 0;
}
