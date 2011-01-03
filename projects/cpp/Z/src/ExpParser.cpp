/*
 * ExpParser.cpp
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#include "ExpParser.h"
#include "Value.h"

using namespace std;

bool ExpParser::IsOpeningParen(char c) {
	return c == '(';
}

bool ExpParser::IsClosingParen(char c) {
	return c == ')';
}

void ExpParser::PopOperation() {

	Operation *op = new Operation(operators_.get(ops_stack_.top()));
	ops_stack_.pop();

	Value* param2 = values_stack_.top();
	values_stack_.pop();
	Value* param1 = values_stack_.top();
	values_stack_.pop();

	op->AddParam(param1);
	op->AddParam(param2);

	values_stack_.push(op);
}

Value* ExpParser::Parse(string line) {

	for (unsigned int i = 0; i < line.length(); i++) {
		char c = line[i];
		if (isdigit(c)) {
			Constant *v = new Constant(line[i] - 48);
			values_stack_.push(v);
		} else if (operators_.IsOperator(c)) {

			Operator* op = operators_.get(c);

			while (!ops_stack_.empty() && !IsOpeningParen(ops_stack_.top())
					&& operators_.get(ops_stack_.top())->precedence()
							>= op->precedence()) {
				PopOperation();
			}
			ops_stack_.push(c);
		} else if (IsOpeningParen(c)) {
			ops_stack_.push(c);
		} else if (IsClosingParen(c)) {
			while (!IsOpeningParen(ops_stack_.top())) {
				PopOperation();
			}
			ops_stack_.pop();
		}

	}

	while (!ops_stack_.empty()) {
		PopOperation();
	}
	Value *exp = values_stack_.top();

	values_stack_.pop();
	return exp;
}
