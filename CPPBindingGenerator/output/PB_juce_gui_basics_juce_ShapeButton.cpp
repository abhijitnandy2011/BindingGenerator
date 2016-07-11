#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_ShapeButton()
{
    class_<ShapeButton>("ShapeButton")
        .def("setShape", &ShapeButton::setShape)
        .def("setColours", &ShapeButton::setColours)
        .def("setOutline", &ShapeButton::setOutline)
        .def("setBorderSize", &ShapeButton::setBorderSize)
        .def("paintButton", &ShapeButton::paintButton)
    ;
}
