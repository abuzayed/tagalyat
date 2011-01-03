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
	std::stack<Value*> values_stack_;
	std::stack<char> ops_stack_;

	bool IsOpeningParen(char c);
	bool IsClosingParen(char c);
	void PopOperation();

public:
	Value* Parse(std::string line);
};

#endif /* EXPPARSER_H_ */
