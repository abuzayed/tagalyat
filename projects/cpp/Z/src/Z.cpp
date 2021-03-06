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
		Value* exp = parser.Parse(line);

		exp->Print(&cout);
		cout << endl;

		cout << exp->GetValue() << endl;

	}

	return 0;

}
