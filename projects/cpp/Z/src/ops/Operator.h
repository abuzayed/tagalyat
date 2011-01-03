/*
 * Operator.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef OPERATOR_H_
#define OPERATOR_H_

#include <list>

class Value;

class Operator {

private:
	const char* name_;
	int precedence_;

public:

	Operator(const char* n, int p);
	const char* name();
	int precedence();

	virtual double Evaluate(std::list<Value*>* params) =0;

};

#endif /* OPERATOR_H_ */
