#include <iostream>

int main() {
  int N, A;
  std::cin >> N >> A;
  for (int i = 0; N >= 500; i++) {
    N = N - 500;
  }
  if (N <= A) {
    std::cout << "Yes" << std::endl;
  }
  else {
    std::cout << "No" << std::endl;
  }
}
