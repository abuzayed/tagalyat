/*
 * Addition.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef MULTIPLICATION_H_
#define MULTIPLICATION_H_

#include <string>

#include "Operator.h"

class Multiplication: public Operator {
public:
	Multiplication() :
		Operator("mul", 20) {
	}

};

#endif /* MULTIPLICATION_H_ */
