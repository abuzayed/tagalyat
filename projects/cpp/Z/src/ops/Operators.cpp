/*
 * Operators.cpp
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#include "Operators.h"
#include "Addition.h"
#include "Subtraction.h"
#include "Multiplication.h"
#include "Division.h"

Operators::Operators() {

	operators_['+'] = new Addition();
	operators_['-'] = new Subtraction();
	operators_['*'] = new Multiplication();
	operators_['/'] = new Division();
}

bool Operators::IsOperator(char c) {
	return operators_.find(c) != operators_.end();
}

Operator* Operators::get(char c) {
	return operators_[c];
}
