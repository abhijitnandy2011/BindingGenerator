#include "stdafx.h"
#include "${moduleName}.h"

void ${moduleName}::wrapForLua(lua_State *L)
{
    using namespace luabind;
    module(L)
        [
	% for c in classes:
			class_<${c.name}>("${c.name}")
    % 	for f in c.functions:
		% if not "hidden" in f.annotations:
            % if f.isVirtual == True:
			.def("${f.name}", pure_virtual(&${c.name}::${f.name}))
            %	else:
			.def("${f.name}", &${c.name}::${f.name})
            % endif
        % endif
    %	endfor
			,
	% endfor
		];
}
