/*
 * Operator.h
 *
 *  Created on: Jan 2, 2011
 *      Author: ahmad
 */

#ifndef OPERATOR_H_
#define OPERATOR_H_

class Operator {

private:
	const char* name_;
	int precedence_;

public:
	Operator(const char* n, int p) {
		name_ = n;
		precedence_ = p;
	}

	const char* name() {
		return name_;
	}

	int precedence() {
		return precedence_;
	}

};

#endif /* OPERATOR_H_ */
