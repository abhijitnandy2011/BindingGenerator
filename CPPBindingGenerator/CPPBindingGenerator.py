"""
This module parses a given directory containing header files and generates appropriate
binding file as per the given template and chosen binding type. 
It uses lib-clang python bindings to parse the file and processes the generated AST.
"""
import sys
import clang.cindex as cind
import os

# Clang default constants & output dir
BINDTYPES_DIR = "bindtypes"
BINDTYPE_CONFIG_FILE = "config.txt"
BIND_PREFIX = "B"
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

def writeToExportedModule(moduleName, exporModuleTpl, functionsList, outputDir):
    """
    Write the binding file for the module
    """
    filePath = os.path.join(outputDir, moduleName + ".cpp")
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

def recursivelyBind(dirPath, makoTpl, index, outDirPath, boundFileNames, prefix):
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
                bindFileName = prefix + cleanDirPath + "_" + fileName
                bindFileName = bindFileName.replace(".h", ".cpp")
                exportFunctionName = fileName.replace(".h", "")
                writeToExportedFile(classes, makoTpl, bindFileName, exportFunctionName, outDirPath)
                boundFileNames.append(fileName)
        for subdir in subdirs:
            recursivelyBind(os.path.join(dirPath, subdir), makoTpl, index, outDirPath, boundFileNames, prefix)

def readConfigFile(configFile):
    """Reads a config file with no section headers and returns a dictionary of key-value pairs"""
    separator = "="
    keys = {}
    # I named your file conf and stored it 
    # in the same directory as the script
    with open(configFile) as f:
        for line in f:
            if separator in line:
                # Find the name and value by splitting the string
                name, value = line.split(separator, 1)
                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                keys[name.strip()] = value.strip()
    return keys


def generateFile():
    """
    This function initializes the CLANG library (based on the environment variable
    CLANG_PATH defined in the system environment variables or he one passed in config.txt), 
    It then parses the given input directory, and generates the bindings based on the 
    supplied template. It raises appropriate errors along the way if it encounters any.
    """

    # Check if passed dir is valid
    if not os.path.exists(sys.argv[1]):
        raise Exception("The directory to pick C++ headers to bind does not exist at: " + sys.argv[1])

    # Read configuration for chosen binding
    chosenBindingPath = os.path.join(BINDTYPES_DIR, sys.argv[3])
    if not os.path.exists(chosenBindingPath):
        raise Exception("There is no configuration file for the chosen binding type at: " + chosenBindingPath)
    configDict = readConfigFile(os.path.join(chosenBindingPath, BINDTYPE_CONFIG_FILE))

    # Check if CLANG is present at the passed path
    clangPath = "./clang"
    if (configDict.has_key("CLANG_PATH")):
        clangPath = configDict["CLANG_PATH"]
    if not os.path.exists(clangPath):
        raise Exception("The path to the CLANG library(libclang.dll or libclang.so file) was not found at " + clangPath +
                        ". The config setting CLANG_PATH needs to be preset in the config file of the required binding type." \
                         " It needs to be set to the directory where the CLANG library is present")
    print("Found CLANG library at " + clangPath)
    
    # Read mako string templates - used for simple string substitution
    from mako.template import Template
    # Do this once here, we do not want to repeatedly do this
    exportModuleTplPath = os.path.join(chosenBindingPath, "exportmodule.mako")
    if not os.path.exists(exportModuleTplPath):
        raise Exception("No module export mako string template found at: " + exportModuleTplPath)

    exportFileTplPath   = os.path.join(chosenBindingPath, "exportfile.mako")
    if not os.path.exists(exportModuleTplPath):
        raise Exception("No cpp file export mako string template found at: " + exportFileTplPath)

    exporModuleTpl = Template(filename = exportModuleTplPath)
    exporFileTpl   = Template(filename = exportFileTplPath)

    print ("Generating " + sys.argv[3] + " bindings for files in " + sys.argv[1] + " and module name " + sys.argv[2])

    # Create the clang index just once & re-use
    libClangDLL = LIB_CLANG_DLL
    if (configDict.has_key("LIB_CLANG_DLL")):
        libClangDLL = configDict["LIB_CLANG_DLL"]
    cind.Config.set_library_file(clangPath + libClangDLL)
    index = cind.Index.create()                 # create index here, we dont want to repeatedly do this

    # Read other config params that may have been passed & required before binding
    prefix = BIND_PREFIX
    if (configDict.has_key("PREFIX")):
        prefix = configDict["PREFIX"]
    
    outputDir = OUTPUT_DIR
    if (configDict.has_key("OUTPUT_DIR")):
        outputDir = configDict["OUTPUT_DIR"]

    # Now parse the dir contents recursively & bind
    boundFileNames = []
    recursivelyBind(sys.argv[1], exporFileTpl, index, outputDir, boundFileNames, prefix)

    # Write the top level module file
    writeToExportedModule(prefix + sys.argv[2], exporModuleTpl, boundFileNames, outputDir)
    
    #printDiagnostics(tu)
    #print_code(classes)
    
if __name__=="__main__":
    if len(sys.argv) < 2:
        print ("Usage - CPPBindingGenerator.py <dirpath-to-bind> <module-name> <binding-type>")
        raise Exception ("Invalid arguments: " + reduce(lambda a, b: a + " " + b, sys.argv, ""))
    else:
        generateFile()

