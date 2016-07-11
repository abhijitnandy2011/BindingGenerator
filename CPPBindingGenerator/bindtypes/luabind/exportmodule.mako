#pragma once

wrap_${moduleName}()
{
% for func in exportFunctions:
    ${func}:wrapForLua();
% endfor
}

