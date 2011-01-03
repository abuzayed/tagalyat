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

};

#endif /* SUBTRACTION_H_ */
