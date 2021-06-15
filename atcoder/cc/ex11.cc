#include <iostream>
#include <string>
using namespace std;

int main() {
  int T, V1, V;
  string op;

  cin >> T >> V1;

  for (int i = 1; i <= T; i++) {
    cin >> op >> V;
    if (op == "+") {
      V1 += V;
      cout << i << ":" << V1 << endl;
    } else if (op == "-") {
      V1 -= V;
      cout << i << ":" << V1 << endl;
    } else if (op == "*") {
      V1 *= V;
      cout << i << ":" << V1 << endl;
    } else if (op == "/") {
      if (V == 0) {
	cout << "error" << endl;
	break;
      }
      V1 /= V;
      cout << i << ":" << V1 << endl;
    }
  }
}
