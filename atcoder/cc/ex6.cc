#include <iostream>

int main() {
  int a, b;
  std::string symbol;
  std::cin >> a >> symbol >> b;

  if (symbol == "+") {
    std::cout << a + b << std::endl;
  }
  else if (symbol == "-") {
    std::cout << a - b << std::endl;
  }
  else if (symbol == "*") {
    std::cout << a * b << std::endl;
  }
  else if (symbol == "/" && b != 0) {
    std::cout << a / b << std::endl;
  }
  else {
    std::cout << "error" << std::endl;
  }
}
