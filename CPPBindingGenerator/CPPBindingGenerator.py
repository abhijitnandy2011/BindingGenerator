"""
This module parses a given .cpp/.h/.c file and generates appropriate
python/lua binding file as per the given template.
It uses lib-clang python bindings to parse the file and process the 
AST generated.
"""
import sys
import clang.cindex as cind
import os

# Mako template file name constants
EXPORT_MODULE_TEMPLATE = "exportmodule.mako"
EXPORT_FILE_TEMPLATE = "exportfile.mako"
CLANG_ENVIRON_VAR = 'CLANG_PATH'
LIB_CLANG_DLL = "/libclang.dll"
OUTPUT_DIR = "output"


def get_annotations(node):
    """
    Get the annotations/attributes associated with the node
    """
    return [c.displayname for c in node.get_children()
            if c.kind == cind.CursorKind.ANNOTATE_ATTR]

# Called for the functions in a class(see next class)
class Function(object):
    """
    A class which holds the function name and any attributes 
    (hidden or not) associated with it
    """
    def __init__(self, cursor):
        #print("Parsing class method:" + cursor.spelling)
        self.name = cursor.spelling
        self.isVirtual = cursor.is_virtual_method()
        self.annotations = get_annotations(cursor)

# Parse a class
class Class(object):
    """
    A class which holds the class declaration and a list of all its
    member functions (within Function object)
    """
    def __init__(self, cursor):
        self.name = cursor.spelling
        print("Parsing class " + self.name)

        # Expose public functions only
        self.functions = [Function(c) for c in cursor.get_children() if (c.kind == cind.CursorKind.CXX_METHOD and c.access_specifier == cind.AccessSpecifier.PUBLIC)]
        self.annotations = get_annotations(cursor)

def build_classes(cursor):
    """
    Builds a list of all classes that are found within the given file
    """
    result = []
    for c in cursor.get_children():
        if (c.kind == cind.CursorKind.CLASS_DECL):
            """and c.location.file.name == sys.argv[1]):"""
            a_class = Class(c)
            result.append(a_class)
        elif c.kind == cind.CursorKind.NAMESPACE:
            child_classes = build_classes(c)
            result.extend(child_classes)

    return result

def node_children(node):
    #return only the children of those nodes that are defined in the current file
    # and not the ones in the include files.
    return (c for c in node.get_children() if True)

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
    print reduce (lambda a, b: a + str(b.severity) + " " + str(b.location) + \
                 " " + b.spelling + " " + b.option + "\n", 
                 (tu.diagnostics, ""))

def writeToExportedModule(moduleName, exporModuleTpl, functionsList):
    """
    Write the binding file for the module
    """
    filePath = os.path.join(OUTPUT_DIR, moduleName + ".cpp")
    out = file (filePath, "w")
    out.write (exporModuleTpl.render(moduleName = moduleName, exportFunctions = functionsList))
    out.close() 

def writeToExportedFile(classes, makoTpl, bindFileName, exportFunctionName, outDirPath):
    """
    Write the binding file based on the given template and the classes and functions
    found in the C file.
    """
    filePath = os.path.join(outDirPath, bindFileName)
    out = file (filePath, "w")
    out.write (makoTpl.render(classes = classes, functionName = exportFunctionName))
    out.close()

def recursivelyBind(dirPath, makoTpl, index, outDirPath, boundFileNames):
    """ Recursively descend dir tree and bind """
    for fpath, subdirs, files in os.walk(dirPath):
        for fileName in files:
            if fileName.endswith('.h') :
                tu = index.parse(path = os.path.join(fpath, fileName), args=['-X', 'c++', '-std=c++11', 
                                                   '-D__BINDING_GENERATOR__'])
                classes = build_classes(tu.cursor)
                cleanDirPath = dirPath.replace(".", "")
                cleanDirPath = cleanDirPath.replace("/", "_")
                cleanDirPath = cleanDirPath.replace("\\", "_")
                bindFileName = "P" + cleanDirPath + "_" + fileName
                bindFileName = bindFileName.replace(".h", ".cpp")
                exportFunctionName = fileName.replace(".h", "")
                writeToExportedFile(classes, makoTpl, bindFileName, exportFunctionName, outDirPath)
                boundFileNames.append(fileName)
        for subdir in subdirs:
            recursivelyBind(os.path.join(dirPath, subdir), makoTpl, index, outDirPath, boundFileNames)



def generateFile():
    """
    This function initializes the CLANG library (based on the environment variable
    CLANG_PATH defined in the system environment variables), parses the given input
    file, and then generates the binding file based on the supplied template.
    It raises appropriate errors along the way if it encounters any.
    """
    clang_path = os.environ.get(CLANG_ENVIRON_VAR, '')
    if not clang_path:
        raise Exception("CLANG_PATH environment variable not defined! Please define " \
                        "it to point to the libclang.dll or libclang.so file " \
                        "installed on the system")

    # Check if passed dir is valid
    if not os.path.exists(sys.argv[1]):
        raise Exception("Provided file or path doesnot exist: " + sys.argv[1])
    
    # Read mako string templates - used for simple string substitution
    from mako.template import Template
    # Do this once here, we do not want to repeatedly do this
    exporModuleTpl = Template(filename = EXPORT_MODULE_TEMPLATE)
    exporFileTpl   = Template(filename = EXPORT_FILE_TEMPLATE)

    print ("Generating python bindings for: " + sys.argv[1])

    # Create the clang index just once & resuse
    cind.Config.set_library_file(clang_path + LIB_CLANG_DLL)
    index = cind.Index.create()                 # create index here, we dont want to repeatedly do this

    # Now parse the dir contents recursively & bind
    boundFileNames = []
    recursivelyBind(sys.argv[1], exporFileTpl, index, OUTPUT_DIR, boundFileNames)

    # Write the top level module file
    writeToExportedModule(sys.argv[2], exporModuleTpl, boundFileNames)
    
    #printDiagnostics(tu)
    #print_code(classes)

    
if __name__=="__main__":
    if len(sys.argv) < 2:
        print ("Usage - CPPBindingGenerator.py <cpp-filename> " \
                "<binding-template> <module-name>")
        raise Exception ("Invalid arguments: " + reduce(lambda a, b: a + " " + b, sys.argv, ""))
    else:
        generateFile()

