#include <iostream>
#include <string>

int main() {
  std::string s;
  int marbles = 0;
  std::cin >> s;
  for (int i = 0; i < s.length(); ++i) {
    if(s[i] == '1') {
      marbles++;
    }
  }
  std::cout << marbles << std::endl;
}
