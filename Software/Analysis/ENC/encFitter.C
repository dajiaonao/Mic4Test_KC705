#include "Minuit2/Minuit2Minimizer.h"
#include "Math/Functor.h"
#include <TMath.h>
#include <vector>
#include <utility>
#include <fstream>
#include <cmath>

const double sqrt2 = TMath::Sqrt(2);

class encFitter{
 public:
  std::vector< std::pair<float, int> > data1;
  double mean, sigma, meanErr, sigmaErr;
  double meanErrU, meanErrD, sigmaErrU, sigmaErrD;
  double minIntL;

  double intL(const double *xx) const{
    // xx[0] is mean and xx[1] is width, xx[2] is the conditional observable, xx[3] is the meansurement
    double val = 1.;
//     for(auto& a: data1){
//       double P = 0.5*(1.+TMath::Erf((a.first-xx[0])/(sqrt2*xx[1])));
//       val *= a.second?P:(1-P);
    for(size_t i=0; i<data1.size(); i++){
      double P = 0.5*(1.+TMath::Erf((data1[i].first-xx[0])/(sqrt2*xx[1])));
      val *= data1[i].second?P:(1-P);
     }

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
   double variable[2] = {0.5,0.3};
 
   min.SetFunction(f);
 
   // Set the free variables to be minimized!
   min.SetVariable(0,"mu",variable[0], step[0]);
   min.SetVariable(1,"sigma",variable[1], step[1]);

   min.SetVariableLimits(0, 0.05, 0.8);
   min.SetVariableLimits(1, 0.0005, 0.2);
 
   min.Minimize(); 

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

   return 0;
  }

  int test(){
    data1.reserve(700);
    int id, v;
    float vL, vH, x;

    std::ifstream fin("ENC_0507_Chip5Col12_scan_normal_try1.dat");
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
