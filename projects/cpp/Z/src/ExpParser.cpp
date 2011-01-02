/*
 * ExpParser.cpp
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#include "ExpParser.h"
#include "Value.h"

using namespace std;

ExpParser::ExpParser() {
	operators['+'] = 10;
	operators['-'] = 10;
	operators['*'] = 20;
	operators['/'] = 20;
}
bool ExpParser::is_operator(char c) {
	return operators.find(c) != operators.end();
}

int ExpParser::precedence(char c) {
	return operators[c];
}

bool ExpParser::is_opening_paren(char c) {
	return c == '(';
}

bool ExpParser::is_closing_paren(char c) {
	return c == ')';
}

void ExpParser::pop_op() {
	Operation *op = new Operation(ops_stack.top());
	ops_stack.pop();

	Value* param2 = values_stack.top();
	values_stack.pop();
	Value* param1 = values_stack.top();
	values_stack.pop();

	op->add_param(param1);
	op->add_param(param2);

	values_stack.push(op);
}

Value* ExpParser::parse(string line) {

	for (unsigned int i = 0; i < line.length(); i++) {
		char c = line[i];
		if (isdigit(c)) {
			Constant *v = new Constant(line[i] - 48);
			values_stack.push(v);
		} else if (is_operator(c)) {
			while (!ops_stack.empty() && !is_opening_paren(ops_stack.top())
					&& precedence(ops_stack.top()) >= precedence(c)) {
				pop_op();
			}
			ops_stack.push(c);
		} else if (is_opening_paren(c)) {
			ops_stack.push(c);
		} else if (is_closing_paren(c)) {
			while (!is_opening_paren(ops_stack.top())) {
				pop_op();
			}
			ops_stack.pop();
		}

	}

	while (!ops_stack.empty()) {
		pop_op();
	}
	Value *exp = values_stack.top();

	values_stack.pop();
	return exp;
}
