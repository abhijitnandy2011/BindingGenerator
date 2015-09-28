"""
This module parses a given .cpp/.h/.c file and generates appropriate
python/lua binding file as per the given template.
It uses lib-clang python bindings to parse the file and process the 
AST generated.
"""
import sys
import clang.cindex as cind
import os

def get_annotations(node):
    """
    Get the annotations/attributes associated with the node
    """
    return [c.displayname for c in node.get_children()
            if c.kind == cind.CursorKind.ANNOTATE_ATTR]

class Function(object):
    """
    A class which holds the function name and any attributes 
    (hidden or not) associated with it
    """
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.annotations = get_annotations(cursor)

class Class(object):
    """
    A class which holds the class declaration and a list of all its
    member functions (within Function object)
    """
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.functions = [Function(c) for c in cursor.get_children() \
                          if (c.kind == cind.CursorKind.CXX_METHOD)]
        self.annotations = get_annotations(cursor)

def build_classes(cursor):
    """
    Builds a list of all classes that are found within the given file
    """
    result = []
    for c in cursor.get_children():
        if (c.kind == cind.CursorKind.CLASS_DECL
            and c.location.file.name == sys.argv[1]):
            a_class = Class(c)
            result.append(a_class)
        elif c.kind == cind.CursorKind.NAMESPACE:
            child_classes = build_classes(c)
            result.extend(child_classes)

    return result

def node_children(node):
    #return only the children of those nodes that are defined in the current file
    # and not the ones in the include files.
    return (c for c in node.get_children() if c.location.file.name == sys.argv[1])

def print_functions(node):
    """
    Print all the functions that were declared/defined in the file that was passed
    """
    if node.kind == cind.CursorKind.FUNCTION_DECL:
        print ('Found %s [line=%s, col=%s]' % (
            node.displayname, node.location.line, node.location.column))

    for c in node.get_children():
        print_functions(c)

def print_node(node):
    """
    Print the AST generated after parsing the file.
    """
    text = node.spelling or node.displayname
    kind = str(node.kind)[str(node.kind).index('.')+1:]
    return '{} {}'.format(kind, text)

def print_code(classes):
    """
    Print all the classes along with their member functions to the console
    """
    for c in classes:
        print ("Class Name: " + c.name)
        print ("Member functions:")
        for function in c.functions:
            print (function.name)

def printDiagnostics(tu):
    """
    Print all warnings/errors encountered while parsing/compiling the file
    """
   # print reduce (lambda a, b: a + str(b.severity) + " " + str(b.location) + \
        #          " " + b.spelling + " " + b.option + "\n", 
        #          (tu.diagnostics, ""))

def writeToFile(classes):
    """
    Write the binding file based on the given template and the classes and functions
    found in the C file.
    """
    from mako.template import Template

    tpl = Template(filename = sys.argv[2])
    pathComp = sys.argv[1].rsplit('.',1)
    filePath = pathComp[0] + '_bind.' + pathComp[1]
    out = file (filePath, "w")
    out.write (tpl.render( classes = classes,
                     module_name = sys.argv[3],
                     include_file = os.path.basename(sys.argv[1])))
    out.close()

def generateFile():
    """
    This function initializes the CLANG library (based on the environment variable
    CLANG_PATH defined in the system environment variables), parses the given input
    file, and then generates the binding file based on the supplied template.
    It raises appropriate errors along the way if it encounters any.
    """
    if not os.path.exists(sys.argv[1]):
        raise Exception("Provided file or path doesnot exist: " + sys.argv[1])

    clang_path = os.environ.get('CLANG_PATH', '')

    if not clang_path:
        raise Exception("CLANG_PATH environment variable not defined! Please define " \
                        "it to point to the libclang.dll or libclang.so file " \
                        "installed on the system")

    print ("Generating python bindings for: " + sys.argv[1])
    cind.Config.set_library_file(clang_path + "/libclang.dll")
    index = cind.Index.create()
    os.chdir(os.path.dirname(sys.argv[1])) #change the current directory to the include directory to avoid compile errors.
    print ("File path after changing the OS directory: " + sys.argv[1])
    tu = index.parse(path = sys.argv[1], args=['-X', 'c++', '-std=c++11', 
                                               '-D__BINDING_GENERATOR__'])
    classes = build_classes(tu.cursor)
    #printDiagnostics(tu)
    writeToFile(classes)
    
if __name__=="__main__":
    if len(sys.argv) < 4:
        print ("Usage - CPPBindingGenerator.py <cpp-filename> " \
                "<binding-template> <module-name>")
        raise Exception ("Invalid arguments: " + reduce(lambda a, b: a + " " + b, sys.argv, ""))
    else:
        generateFile()

