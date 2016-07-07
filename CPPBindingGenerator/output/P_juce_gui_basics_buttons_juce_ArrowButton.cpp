#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_ArrowButton()
{
    class_<ArrowButton>("ArrowButton")
        .def("paintButton", &ArrowButton::paintButton)
    ;
}
