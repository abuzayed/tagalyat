/*
 * Addition.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef SUBTRACTION_H_
#define SUBTRACTION_H_

#include <string>

#include "Operator.h"

class Subtraction: public Operator {

public:

	Subtraction() :
		Operator("sub", 10) {
	}

	double Evaluate(std::list<Value*>* params) {
		return params->front()->GetValue() - params->back()->GetValue();
	}

};

#endif /* SUBTRACTION_H_ */
