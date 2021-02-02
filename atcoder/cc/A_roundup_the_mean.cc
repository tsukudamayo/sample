#include <iostream>
#include <cmath>

int main() {
  double a, b;
  std::cin >> a;
  std::cin >> b;
  double mean = (a + b)/2;
  int roundup = std::ceil(mean);
  std::cout << roundup << std::endl;
}
