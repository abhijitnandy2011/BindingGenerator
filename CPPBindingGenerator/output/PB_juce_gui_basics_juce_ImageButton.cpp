#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_ImageButton()
{
    class_<ImageButton>("ImageButton")
        .def("setImages", &ImageButton::setImages)
        .def("getNormalImage", &ImageButton::getNormalImage)
        .def("getOverImage", &ImageButton::getOverImage)
        .def("getDownImage", &ImageButton::getDownImage)
    ;
}
