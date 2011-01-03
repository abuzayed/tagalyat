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
	virtual double GetValue() =0;
	virtual void Print(std::ostream *out) =0;
};

class Constant: public Value {
	double value_;
public:
	Constant(double v);
	double GetValue();
	void Print(std::ostream *out);
};

class Operation: public Value {

	Operator* op_;
	std::list<Value*> params_;

public:

	Operation(Operator* op);
	void AddParam(Value* param);
	double GetValue();
	void Print(std::ostream *out);
};

#endif /* VALUE_H_ */
