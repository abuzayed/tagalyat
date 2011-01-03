/*
 * Addition.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef ADDITION_H_
#define ADDITION_H_

#include <string>

#include "Operator.h"

class Addition: public Operator {
public:
	Addition() :
		Operator("add", 10) {
	}

};

#endif /* ADDITION_H_ */
