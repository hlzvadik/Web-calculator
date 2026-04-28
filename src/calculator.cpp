#include <iostream>
#include <string>
#include <cstring>
#include "../cpp-core/include/mylib/calculator/calculator.hpp"
#include "../cpp-core/include/mylib/queue/myqueue.hpp"
#include "../cpp-core/include/mylib/stack/mystack.hpp"
#include "../cpp-core/include/mylib/calculator/mathoperations/mathoperations.hpp"

namespace goltsov
{
  using lli = long long int;

  lli priority(std::string a)
  {
    if (a == "-" || a == "+")
    {
      return 1;
    }
    else if (a == "%")
    {
      return 2;
    }
    else if (a == "*" || a == "/")
    {
      return 3;
    }
    else if (a == "##")
    {
      return 4;
    }
    else
    {
      return -1;
    }
  }

  goltsov::Queue< std::string > converToPostfix(goltsov::Queue< std::string > a)
  {
    goltsov::Queue< std::string > postfix;
    goltsov::Stack< std::string > op_and_br;
    std::string prev = " ";
    while(!a.empty())
    {
      if (isdigit(a.front()[0]))
      {
        if (prev != " " && isdigit(prev[0]))
        {
          throw std::logic_error("Bad input expression");
        }
        postfix.push(a.front());
      }
      else if (a.front() == "(")
      {
        if (prev != " " && (isdigit(prev[0]) || prev == ")"))
        {
          throw std::logic_error("Bad input expression");
        }
        op_and_br.push(a.front());
      }
      else if (a.front() == ")")
      {
        if ((prev != " " && !isdigit(prev[0])) && prev != ")" || prev == "(")
        {
          throw std::logic_error("Bad input expression");
        }
        while(!op_and_br.empty() && op_and_br.front() != "(")
        {
          postfix.push(op_and_br.front());
          op_and_br.drop();
        }
        if (op_and_br.empty())
        {
          throw std::logic_error("Bad input expression");
        }
        op_and_br.drop();
      }
      else
      {
        if (prev != " " && !isdigit(prev[0]) && prev != ")")
        {
          throw std::logic_error("Bad input expression");
        }
        if (op_and_br.empty() || priority(a.front()) > priority(op_and_br.front()))
        {
          op_and_br.push(a.front());
        }
        else
        {
          while (!op_and_br.empty()
            && (priority(a.front()) <= priority(op_and_br.front())) && op_and_br.front() != "(")
          {
            postfix.push(op_and_br.front());
            op_and_br.drop();
          }
          op_and_br.push(a.front());
        }
      }
      prev = a.front();
      a.drop();
    }
    while(!op_and_br.empty())
    {
      postfix.push(op_and_br.front());
      op_and_br.drop();
    }
    return postfix;
  }

  lli convertStringToLLI(std::string a)
  {
    lli res = 0;
    for (size_t i = 0; i < a.size(); ++i)
    {
      res = res * 10 + (a[i] - '0');
    }
    return res;
  }

  lli solve(goltsov::Queue< std::string > postfix)
  {
    goltsov::Stack< lli > result;
    while (!postfix.empty())
    {
      lli a, b;
      std::string operation;
      while (!postfix.empty() && isdigit(postfix.front()[0]))
      {
        result.push(convertStringToLLI(postfix.front()));
        postfix.drop();
      }
      try
      {
        operation = postfix.front();
        postfix.drop();
      }
      catch (...)
      {
        if (result.size() != 1)
        {
          throw;
        }
        else
        {
          return result.front();
        }
      }
      a = result.front();
      result.drop();
      b = result.front();
      result.drop();
      if (operation == "+")
      {
        result.push(goltsov::addition(b, a));
      }
      else if (operation == "-")
      {
        result.push(goltsov::subtraction(b, a));
      }
      else if (operation == "*")
      {
        result.push(goltsov::multiplication(b, a));
      }
      else if (operation == "/")
      {
        result.push(goltsov::division(b, a));
      }
      else if (operation == "%")
      {
        result.push(goltsov::remOfDiv(b, a));
      }
      else if (operation == "##")
      {
        result.push(goltsov::concatenation(b, a));
      }
    }
    return result.front();
  }

  goltsov::Queue< std::string > parsing(std::string example)
  {
    goltsov::Queue< std::string > inf;
    std::string numb = "";
    char prev = ' ';
    for (size_t i = 0; i < example.size(); ++i)
    {
      if (example[i] == ' ')
      {
        if (prev == ' ')
        {
          continue;
        }
        else
        {
          if (isdigit(prev))
          {
            inf.push(numb);
            numb = "";
            prev = ' ';
          }
          else
          {
            prev = ' ';
          }
        }
      }
      else if (isdigit(example[i]))
      {
        if (!inf.empty() && isdigit(inf.back()[0]))
        {
          throw std::logic_error("Bad input expression");
        }
        numb += example[i];
        prev = example[i];
      }
      else if (example[i] == ')')
      {
        if (isdigit(prev))
        {
          inf.push(numb);
          numb = "";
        }
        inf.push(std::string(1, example[i]));
        prev = example[i];
      }
      else if (example[i] == '(')
      {
        if (isdigit(prev))
        {
          inf.push(numb);
          numb = "";
          inf.push("*");
        }
        else if (!inf.empty() && (isdigit(inf.back()[0]) || inf.back() == ")"))
        {
          inf.push("*");
        }
        inf.push(std::string(1, example[i]));
        prev = example[i];
      }
      else if (example[i] == '-' or example[i] == '+')
      {
        if (isdigit(prev))
        {
          inf.push(numb);
          numb = "";
          inf.push(std::string(1, example[i]));
          prev = example[i];
        }
        else if (inf.empty() || inf.back() == "(")
        {
          inf.push("0");
          inf.push(std::string(1, example[i]));
          prev = example[i];
        }
        else if (inf.back() == ")" || prev == ' ')
        {
          inf.push(std::string(1, example[i]));
          prev = example[i];
        }
        else
        {
          throw std::logic_error("Bad input expression");
        }
      }
      else
      {
        if (isdigit(prev))
        {
          inf.push(numb);
          numb = "";
          inf.push(std::string(1, example[i]));
          prev = example[i];
        }
        else if (inf.back() == ")" || prev == ' ')
        {
          inf.push(std::string(1, example[i]));
          prev = example[i];
        }
        else
        {
          throw std::logic_error("Bad input expression");
        }
      }
    }
    if (numb.size())
    {
      inf.push(numb);
    }
    return inf;
  }

  lli eval(std::string example)
  {
    return solve(converToPostfix(parsing(example)));
  }
}
