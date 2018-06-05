#include "Minuit2/Minuit2Minimizer.h"
#include "Math/Functor.h"
#include <TMath.h>
#include <vector>
#include <utility>
#include <fstream>
#include <cmath>
using namespace std;
const double sqrt2 = TMath::Sqrt(2);

class encFitter{
 public:
  std::vector< std::pair<float, int> > data1;
  double mean, sigma, meanErr, sigmaErr;
  double meanErrU, meanErrD, sigmaErrU, sigmaErrD;
  double minIntL;
  float mean0, meanD, meanU;
  float sigma0, sigmaD, sigmaU;

  encFitter(){
    data1.reserve(1000);
    mean0 = 0.5;
    sigma0 = 0.1;
    meanD = 0.05;
    meanU = 0.8;
    sigmaD = 0.001;
    sigmaU = 0.05;
  };

  void clearData(){
    data1.clear();
    cout << "Data cleared: size= " << data1.size() << endl;
  }

  void showData(size_t n, size_t m=0){
    if(n>data1.size()) n = data1.size();
    cout << "------- data1:" << data1.size() << " -------" << endl;
    for(size_t i=m; i<n; i++){
      cout << i << " " << data1[i].first << " " << data1[i].second << endl;
     }
    cout << "------- End -------" << endl;
   }

  double intL(const double *xx) const{
    // xx[0] is mean and xx[1] is width
    double val = 1.;
//     for(auto& a: data1){
//       double P = 0.5*(1.+TMath::Erf((a.first-xx[0])/(sqrt2*xx[1])));
//       val *= a.second?P:(1-P);
    for(size_t i=0; i<data1.size(); i++){
      double P = 0.5*(1.+TMath::Erf((data1[i].first-xx[0])/(sqrt2*xx[1])));
      val *= data1[i].second?P:(1-P);
//       cout << i << ": " << data1[i].first << " & " << data1[i].second << -2*log(val) << endl;
     }
//     cout << xx[0] << " " << xx[1] << "->" << -2*log(val) << endl;
    return -2*log(val);
   }

  void addData(float x, int d){
    data1.push_back(std::make_pair(x, d));
   }

  int fit(){
   // Choose method upon creation between:
   // kMigrad, kSimplex, kCombined, 
   // kScan, kFumili
   ROOT::Minuit2::Minuit2Minimizer min ( ROOT::Minuit2::kMigrad );
 
   min.SetMaxFunctionCalls(1000000);
   min.SetMaxIterations(100000);
   min.SetTolerance(0.001);
 
   ROOT::Math::Functor f(this, &encFitter::intL,2); 
   double step[2] = {0.0001,0.0001};
//    double variable[2] = {0.35,0.3};
//    double variable[2] = {0.1003,0.004406};
//    double variable[2] = {0.14,0.006};
   double variable[2] = {mean0,sigma0};
 
   min.SetFunction(f);
 
   // Set the free variables to be minimized!
   min.SetVariable(0,"mu",variable[0], step[0]);
   min.SetVariable(1,"sigma",variable[1], step[1]);

   min.SetVariableLimits(0, meanD, meanU);
   min.SetVariableLimits(1, sigmaD, sigmaU);
 
   int ret = min.Minimize()?0:min.Status(); 

   /// check the results    
   const double *xs = min.X();
   mean = xs[0];
   sigma = xs[1];
   const double *errs = min.Errors();
   meanErr = errs[0];
   sigmaErr = errs[1];
   min.GetMinosError(0, meanErrD, meanErrU);
   min.GetMinosError(1, sigmaErrD, sigmaErrU);
   minIntL = intL(xs);

   cout << "Minimum: f(" << xs[0] << "," << xs[1] << "): " 
        << minIntL << endl;
   cout << "mean error:" << meanErr << " " << meanErrD << " " << meanErrU << std::endl;
   cout << "width error:" << sigmaErr << " " << sigmaErrD << " " << sigmaErrU << std::endl;

//1.00301e-01   5.03571e-04   2.38270e-07   1.01821e+00
//   2  p1           4.40609e-03
//    double par2[2] = {1.00301e-01, 4.40609e-03};
//    cout << intL(par2) << endl;

   return ret;
  }

  int test(string fname="ENC_0507_Chip5Col12_scan_normal_try1.dat"){
    data1.reserve(700);
    int id, v;
    float vL, vH;

    std::ifstream fin(fname.c_str());
    while(fin){
      fin >> id >> vL >> vH >> v;
      data1.push_back(std::make_pair(vH-vL, v));
     }

    return fit();
  }
};

int minimize_test(){
//   auto en1 = new encFitter();
  encFitter* en1 = new encFitter();
  en1->test();

  return 0;
}
