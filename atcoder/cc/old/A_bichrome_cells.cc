#include <iostream>

int main() {
  int N, cell, white, target;
  std::cin >> N;
  std::cin >> white;
  cell = N*N;
  target = cell - white;
  std::cout << target << std::endl;
}
