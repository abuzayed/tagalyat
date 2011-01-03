/*
 * Operator.cpp
 *
 *  Created on: Jan 3, 2011
 *      Author: ahmad
 */

#include "Operator.h"

Operator::Operator(const char* n, int p) {
	name_ = n;
	precedence_ = p;
}

const char* Operator::name() {
	return name_;
}

int Operator::precedence() {
	return precedence_;
}
