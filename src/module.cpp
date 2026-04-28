#include <pybind11/pybind11.h>
#include <string>
#include "../cpp-core/include/mylib/calculator/calculator.hpp"

namespace py = pybind11;

PYBIND11_MODULE(calculator_module, m)
{
  m.doc() = "Calculator module with parsing";

  m.def("eval", &goltsov::eval, "Evaluate a math-expression string", py::arg("expression"));
}
