/*
 * Value.cpp
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */
#include "Value.h"

#include <iostream>
#include <list>

using namespace std;

Constant::Constant(double v) {
	value = v;
}

double Constant::get_value() {
	return value;
}

void Constant::print(std::ostream *out) {
	(*out) << value;
}

Operation::Operation(char n) {
	name = n;
}

void Operation::add_param(Value* param) {
	params.push_back(param);
}

double Operation::get_value() {
	return -1;
}

void Operation::print(std::ostream *out) {
	(*out) << name << "(";

	for (list<Value*>::iterator it = params.begin(); it != params.end(); it++) {
		(*it)->print(out);
		if ((*it) != params.back())
			(*out) << ",";
	}

	(*out) << ")";

}

