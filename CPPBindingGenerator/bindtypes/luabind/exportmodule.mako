#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

BOOST_PYTHON_MODULE(${moduleName})
{
% for func in exportFunctions:
    export_${func}();
% endfor
}

