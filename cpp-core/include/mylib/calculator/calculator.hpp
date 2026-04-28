#ifndef CALCULATOR_HPP
#define CALCULATOR_HPP
#include <string>
#include "../queue/myqueue.hpp"

namespace goltsov
{
  long long int priority(std::string a);
  goltsov::Queue< std::string > converToPostfix(goltsov::Queue< std::string > a);
  long long int convertStringToLLI(std::string a);
  long long int eval(goltsov::Queue< std::string > postfix);
}

#endif
