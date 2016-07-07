#pragma once
#include <boost/python.hpp>
#include "${include_file}"

using namespace boost::python;

BOOST_PYTHON_MODULE(${moduleName})
{
% for c in exportFunctions:
    export${c.name}();
% endfor
}

