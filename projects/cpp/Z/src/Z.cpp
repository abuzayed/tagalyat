#include <iostream>

#include "Value.h"
#include "ExpParser.h"

using namespace std;

int main() {

	ExpParser parser;

	while (true) {

		cout << "> ";

		string line;
		cin >> line;

		cout << "line: \"" << line << "\"" << endl;
		Value* exp = parser.parse(line);

		exp->print(&cout);

		cout << endl;

	}

	return 0;

}
