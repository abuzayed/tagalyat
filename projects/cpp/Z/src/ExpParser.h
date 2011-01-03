/*
 * ExpParser.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef EXPPARSER_H_
#define EXPPARSER_H_

#include <map>
#include <stack>

#include "Value.h"
#include "ops/Operators.h"

class ExpParser {
private:
	Operators operators_;
	std::stack<Value*> values_stack;
	std::stack<char> ops_stack;

	bool is_opening_paren(char c);
	bool is_closing_paren(char c);
	void pop_op();

public:
	Value* parse(std::string line);
};

#endif /* EXPPARSER_H_ */
