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
const double h = 0.001;

typedef long long ll;

double f(double x) {
	return 5 * x * x * x * x - 22.4 * x * x * x + 15.85272 * x * x + 24.161472 * x - 23.4824832;
}

double f_p(double x) {
	return (f(x + h) - f(x)) / h;
}

double f_p_p(double x) {
	return (f(x + h) - f(x) * 2 + f(x - h)) / (h * h);
}

double equal(double a, double b) {
	return abs(a - b) <= 0.000001;
}

double newton_raphson(double x) {
	double prev;

	do {
		prev = x;
		x = x - f_p(x) / f_p_p(x);
	} while (!equal(x, prev));
	return x;
}

int main(void)
{
	cout << fixed;
	cout.precision(10);

	double guess[] = { -2, 4 };

	for (auto d : guess) {
		cout << newton_raphson(d) << "\n";
	}
}