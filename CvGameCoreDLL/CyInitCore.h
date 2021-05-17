#pragma once

#ifndef CY_INIT_CORE_H
#define CY_INIT_CORE_H

// ccgs: Adapter class for exposing CvInitCore functions to Python
#include <boost/python/list.hpp>
#include <boost/python/tuple.hpp>
namespace python = boost::python;

class CyInitCore
{
public:
	CyInitCore();

	int getGameSpeed();
	void setGameSpeed(int iGameSpeed);

private:
	CvInitCore& m_kInitCore;
};

#endif
