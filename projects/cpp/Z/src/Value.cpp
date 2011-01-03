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
	value_ = v;
}

double Constant::GetValue() {
	return value_;
}

void Constant::Print(std::ostream *out) {
	(*out) << value_;
}

Operation::Operation(Operator* op) {
	op_ = op;
}

void Operation::AddParam(Value* param) {
	params_.push_back(param);
}

double Operation::GetValue() {
	return -1;
}

void Operation::Print(std::ostream *out) {
	(*out) << op_->name() << "(";

	for (list<Value*>::iterator it = params_.begin(); it != params_.end(); it++) {
		(*it)->Print(out);
		if ((*it) != params_.back())
			(*out) << ",";
	}

	(*out) << ")";

}

