#include <iostream>
#include "./cpp-core/include/mylib/calculator/calculator.hpp"
#include <string>

int main()
{
  std::string a;
  std::getline(std::cin, a);
  std::cout << goltsov::eval(a) << '\n';
}