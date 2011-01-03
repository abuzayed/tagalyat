/*
 * Addition.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef DIVISION_H_
#define DIVISION_H_

#include <string>

#include "Operator.h"

class Division: public Operator {
public:
	Division() :
		Operator("div", 20) {
	}

};

#endif /* DIVISION_H_ */
