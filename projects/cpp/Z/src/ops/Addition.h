/*
 * Addition.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef ADDITION_H_
#define ADDITION_H_

#include <string>
#include <list>

#include "Operator.h"
#include "../Value.h"

class Addition: public Operator {
public:
	Addition() :
		Operator("add", 10) {
	}

	double Evaluate(std::list<Value*>* params) {
		return params->front()->GetValue() + params->back()->GetValue();
	}

};

#endif /* ADDITION_H_ */
