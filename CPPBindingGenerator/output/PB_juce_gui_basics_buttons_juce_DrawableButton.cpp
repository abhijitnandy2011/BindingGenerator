#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_DrawableButton()
{
    class_<DrawableButton>("DrawableButton")
        .def("setImages", &DrawableButton::setImages)
        .def("setButtonStyle", &DrawableButton::setButtonStyle)
        .def("getStyle", &DrawableButton::getStyle)
        .def("setEdgeIndent", &DrawableButton::setEdgeIndent)
        .def("getCurrentImage", &DrawableButton::getCurrentImage)
        .def("getNormalImage", &DrawableButton::getNormalImage)
        .def("getOverImage", &DrawableButton::getOverImage)
        .def("getDownImage", &DrawableButton::getDownImage)
        .def("paintButton", &DrawableButton::paintButton)
        .def("buttonStateChanged", &DrawableButton::buttonStateChanged)
        .def("resized", &DrawableButton::resized)
        .def("enablementChanged", &DrawableButton::enablementChanged)
        .def("colourChanged", &DrawableButton::colourChanged)
    ;
}
