#include <iostream>
using namespace std;

int main() {
  int A, B;
  cin >> A >> B;

  cout << "A:";
  for (int i = 0; i < A; i++) {
    cout << "]";
  }
  cout << endl;

  cout<< "B:";
  for (int j = 0; j < B; j++) {
    cout << "]";
  }
  cout << endl;
}
