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
	return 5 * x * x * x * x - 22.4 * x * x * x + 15.85272 * x * x + 24.161472 * x - 23.4824832;
}

double equal(double a, double b) {
	return abs(a - b) <= 0.00001;
}

double bisection(double minus, double plus) {
	double ans = NAN;
	if (equal(f(minus), 0)) {
		return minus;
	}
	if (equal(f(plus), 0)) {
		return plus;
	}
	while (!equal(minus, plus)) {
		ans = (minus + plus) / 2;
		double val = f(ans);
		if (equal(val, 0)) {
			return ans;
		}
		else if (val > 0) {
			plus = ans;
		}
		else {
			minus = ans;
		}
	}
	return ans;
}

int main(void)
{
	cout << fixed;
	cout.precision(10);
	for (double i = -2.0001; i <= 4.0001; i += 0.0001) {
		double a = i, b = i + 0.0001;

		if (f(a) * f(b) > 0) {
			continue;
		}
		else if (f(a) > 0) {
			swap(a, b);
		}
		cout << bisection(a, b) << "\n";
	}
}