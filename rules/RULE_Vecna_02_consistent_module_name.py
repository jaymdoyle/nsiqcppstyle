"""
Start the function name should not have any underbars in its name

== Violation ==

    bool Check_Sth() { <== Violation. The function name contains an underbar character.
        return false;
    }
    
    bool _CheckSth() { <== Violation. The function name starts with uppercase C.
        return false;
    }
    
== Good ==

    bool isSth() { <== OK.
        return true;
    }
   
"""

from nsiqcppstyle_rulehelper import  *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
import re

module_name_list = {}

prog = re.compile("^([^A-Z]+)([A-Z0-9_].*)")

def RunFunctionNameChecker(lexer, fullName, decl, contextStack, context, filename) :
    t = lexer.GetCurToken()
    value = t.value
    result = prog.search(value)
    function_module_name = result.group(1);

    result = prog.search(filename)
    file_module_name = result.group(1);
    
    if(function_module_name != file_module_name) :
        nsiqcppstyle_reporter.Error(t, __name__, "Inconsistent module naming for function %s in %s" % (value, filename))         


def RunRule(lexer, fullName, decl, contextStack, context) :
    t = lexer.GetCurToken()
    value = t.value
    result = prog.search(value)
    module_name = result.group(1);
    
    if module_name_list.has_key(module_name) :
        module_name_list[module_name] = module_name_list[module_name] + 1
    else :
        module_name_list[module_name] = 1
    
def ResetModuleNameList(lexer, filename, dirname) :
    module_name_list = {}

def RunModuleNameAnalysis(lexer, filename, dirname) :
    highest_hit_count = 0
    
    print "JAY_RULE : start " + filename
    if(len(module_name_list) > 1) :

        # Find the most frequently used module name in file
        for key, value in module_name_list.iteritems() :
            print "J(%s:%s:%d)" % (filename, key, value )
            if (value > highest_hit_count) :
                highest_hit_count = value
                file_module_name = key
        
        print "JAY_RULE Module name %s should be used in %s" %  (key , filename)    
        nsiqcppstyle_reporter.Error(t, __name__, "Inconsistent module naming for functions in file. The most frequently used module name was %s in %s" % (key, filename))         
    
    else :
        print "JAY_RULE: OK"

#ruleManager.AddFileStartRule(ResetModuleNameList)
#ruleManager.AddFunctionNameRule(RunRule)
#ruleManager.AddFileEndRule(RunModuleNameAnalysis)
ruleManager.AddFunctionNameRuleWithFilenameContext(RunFunctionNameChecker)

###########################################################################################
# Unit Test
###########################################################################################

from nsiqunittest.nsiqcppstyle_unittestbase import *
class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)
    
    def test1(self):
        self.Analyze("test/thisFile.c", 
"""
bool Can_Have() {
}""")
        assert CheckErrorContent(__name__)    
    def test2(self):
        self.Analyze("test/thisFile.c", 
"""
bool CTEST:Can_Have() {
}""")
        assert CheckErrorContent(__name__)    
    def test3(self):
        self.Analyze("test/thisFile.c", 
"""
extern bool CTEST:canHave() {
}""")
        assert not CheckErrorContent(__name__)    
    def test4(self):
        self.Analyze("test/thisFile.c", 
"""
extern int CTEST:_CanHave() {
}""")
        assert CheckErrorContent(__name__)    
