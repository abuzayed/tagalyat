#include <iostream>
#include <map>
#include <stack>

using namespace std;

map<char, int> operators;

bool is_operator(char c) {
	return operators.find(c) != operators.end();
}

int precedence(char c) {
	return operators[c];
}

bool is_opening_paren(char c) {
	return c == '(';
}

bool is_closing_paren(char c) {
	return c == ')';
}

int main() {

	operators['+'] = 10;
	operators['-'] = 10;
	operators['*'] = 20;
	operators['/'] = 20;

	while (true) {

		cout << "> ";

		string line;
		cin >> line;

		cout << "line: \"" << line << "\"" << endl;

		stack<char> stack;
		string postfix;

		for (unsigned int i = 0; i < line.length(); i++) {
			char c = line[i];

			if (isdigit(c)) {
				postfix += line[i];

			} else if (is_operator(c)) {

				while (!stack.empty() && !is_opening_paren(stack.top())
						&& precedence(stack.top()) >= precedence(c)) {
					postfix += stack.top();
					stack.pop();
				}

				stack.push(c);

			} else if (is_opening_paren(c)) {
				stack.push(c);

			} else if (is_closing_paren(c)) {

				while (!is_opening_paren(stack.top())) {
					postfix += stack.top();
					stack.pop();
				}
				stack.pop();

			}

		}

		while (!stack.empty()) {
			postfix += stack.top();
			stack.pop();
		}

		cout << "postfix: \"" << postfix << "\"" << endl;

	}

	return 0;

}
