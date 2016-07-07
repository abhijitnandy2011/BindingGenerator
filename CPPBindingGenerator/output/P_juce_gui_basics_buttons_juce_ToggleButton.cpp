#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_ToggleButton()
{
    class_<ToggleButton>("ToggleButton")
        .def("changeWidthToFitText", &ToggleButton::changeWidthToFitText)
    ;
}
