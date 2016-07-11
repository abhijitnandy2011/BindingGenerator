#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void exportjuce_Button()
{
    class_<Button>("Button")
        .def("setButtonText", &Button::setButtonText)
        .def("getButtonText", &Button::getButtonText)
        .def("isDown", &Button::isDown)
        .def("isOver", &Button::isOver)
        .def("setToggleState", &Button::setToggleState)
        .def("getToggleState", &Button::getToggleState)
        .def("getToggleStateValue", &Button::getToggleStateValue)
        .def("setClickingTogglesState", &Button::setClickingTogglesState)
        .def("getClickingTogglesState", &Button::getClickingTogglesState)
        .def("setRadioGroupId", &Button::setRadioGroupId)
        .def("getRadioGroupId", &Button::getRadioGroupId)
        .def("addListener", &Button::addListener)
        .def("removeListener", &Button::removeListener)
        .def("triggerClick", pure_virtual(&Button::triggerClick))
        .def("setCommandToTrigger", &Button::setCommandToTrigger)
        .def("getCommandID", &Button::getCommandID)
        .def("addShortcut", &Button::addShortcut)
        .def("clearShortcuts", &Button::clearShortcuts)
        .def("isRegisteredForShortcut", &Button::isRegisteredForShortcut)
        .def("setRepeatSpeed", &Button::setRepeatSpeed)
        .def("setTriggeredOnMouseDown", &Button::setTriggeredOnMouseDown)
        .def("getMillisecondsSinceButtonDown", &Button::getMillisecondsSinceButtonDown)
        .def("setTooltip", &Button::setTooltip)
        .def("setConnectedEdges", &Button::setConnectedEdges)
        .def("getConnectedEdgeFlags", &Button::getConnectedEdgeFlags)
        .def("isConnectedOnLeft", &Button::isConnectedOnLeft)
        .def("isConnectedOnRight", &Button::isConnectedOnRight)
        .def("isConnectedOnTop", &Button::isConnectedOnTop)
        .def("isConnectedOnBottom", &Button::isConnectedOnBottom)
        .def("setState", &Button::setState)
        .def("getState", &Button::getState)
        .def("JUCE_DEPRECATED", &Button::JUCE_DEPRECATED)
    ;
}
