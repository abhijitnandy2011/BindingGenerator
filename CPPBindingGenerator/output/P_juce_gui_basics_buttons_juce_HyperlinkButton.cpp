#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_HyperlinkButton()
{
    class_<HyperlinkButton>("HyperlinkButton")
        .def("setFont", &HyperlinkButton::setFont)
        .def("setURL", &HyperlinkButton::setURL)
        .def("getURL", &HyperlinkButton::getURL)
        .def("changeWidthToFitText", &HyperlinkButton::changeWidthToFitText)
    ;
}
