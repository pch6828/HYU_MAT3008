#include<cstdio>
#include<climits>
#include<cmath>
#include<cstdlib>
#include<cstring>
#include<cassert>
#include<vector>
#include<iostream>
#include<fstream>
#include<sstream>
#include<queue>
#include<stack>
#include<set>
#include<map>
#include<unordered_map>
#include<unordered_set>
#include<deque>
#include<list>
#include<string>
#include<bitset>
#include<algorithm>
#include<functional>
#include<numeric>
#include<random>
#include<complex>

using namespace std;

const double PI = acos(-1);

typedef long long ll;

double f(double x) {
	return 5 * x * x * x * x 
		- 22.4 * x * x * x 
		+ 15.85272 * x * x 
		+ 24.161472 * x 
		- 23.4824832;
}

double f_p(double x) {
	return 20 * x * x * x 
		- 67.2 * x * x 
		+ 31.70544 * x 
		+ 24.161472;
}

double equal(double a, double b) {
	return abs(a - b) <= 0.00001;
}

double newton_raphson(double x) {
	double prev;

	do {
		prev = x;
		x = x - f(x) / f_p(x);
	} while (!equal(x, prev));
	return x;
}

int main(void)
{
	cout << fixed;
	cout.precision(10);

	double guess[] = { -1, 1, 1.5, 3 };
	for (auto d : guess) {
		cout << newton_raphson(d) << "\n";
	}
}