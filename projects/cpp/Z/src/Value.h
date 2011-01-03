/*
 * Value.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef VALUE_H_
#define VALUE_H_

#include <list>
#include <iostream>

#include "ops/Operator.h"

class Value {
public:
	virtual double get_value() =0;
	virtual void print(std::ostream *out) =0;
};

class Constant: public Value {
	double value;
public:
	Constant(double v);
	double get_value();
	void print(std::ostream *out);
};

class Operation: public Value {

	Operator* op_;
	std::list<Value*> params;

public:

	Operation(Operator* op);
	void add_param(Value* param);
	double get_value();
	void print(std::ostream *out);
};

#endif /* VALUE_H_ */
