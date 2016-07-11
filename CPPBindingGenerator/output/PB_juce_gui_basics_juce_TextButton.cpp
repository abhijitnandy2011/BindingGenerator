#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_TextButton()
{
    class_<TextButton>("TextButton")
        .def("changeWidthToFitText", &TextButton::changeWidthToFitText)
        .def("changeWidthToFitText", &TextButton::changeWidthToFitText)
        .def("getBestWidthForHeight", &TextButton::getBestWidthForHeight)
        .def("paintButton", &TextButton::paintButton)
        .def("colourChanged", &TextButton::colourChanged)
    ;
}
