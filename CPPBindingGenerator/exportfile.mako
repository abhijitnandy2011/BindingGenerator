#pragma once
#include <boost/python.hpp>
#include "../JuceLibraryCode/JuceHeader.h"

using namespace boost::python;

void export${functionName}()
{
% for c in classes:
    class_<${c.name}>("${c.name}")
    % for f in c.functions:
        % if not "hidden" in f.annotations:
        .def("${f.name}", &${c.name}::${f.name})
        % endif
    % endfor
    ;
% endfor
}
