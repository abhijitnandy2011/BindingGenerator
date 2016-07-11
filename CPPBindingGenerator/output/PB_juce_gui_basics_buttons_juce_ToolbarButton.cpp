#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_ToolbarButton()
{
    class_<ToolbarButton>("ToolbarButton")
        .def("getToolbarItemSizes", &ToolbarButton::getToolbarItemSizes)
        .def("paintButtonArea", &ToolbarButton::paintButtonArea)
        .def("contentAreaChanged", &ToolbarButton::contentAreaChanged)
        .def("buttonStateChanged", &ToolbarButton::buttonStateChanged)
        .def("resized", &ToolbarButton::resized)
        .def("enablementChanged", &ToolbarButton::enablementChanged)
    ;
}
