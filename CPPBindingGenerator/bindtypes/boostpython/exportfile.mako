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
            % if f.isVirtual == True:
        .def("${f.name}", pure_virtual(&${c.name}::${f.name}))
            % else:
        .def("${f.name}", &${c.name}::${f.name})
            % endif
        % endif
    % endfor
    ;
% endfor
}
