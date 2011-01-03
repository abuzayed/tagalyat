/*
 * Operators.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef OPERATORS_H_
#define OPERATORS_H_

#include <map>

#include "Operator.h"

class Operators {
private:
	std::map<char, Operator*> operators_;
public:
	Operators();
	bool IsOperator(char c);
	Operator* get(char c);
};

#endif /* OPERATORS_H_ */
