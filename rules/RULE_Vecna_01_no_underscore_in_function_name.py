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

def RunRule(lexer, fullName, decl, contextStack, context) :
    t = lexer.GetCurToken()
    value = t.value
    if Search("[_]", value)  :
        nsiqcppstyle_reporter.Error(t, __name__, "Do not use underbars in function name(%s). Use camel case instead" % fullName)         

ruleManager.AddFunctionNameRule(RunRule)


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
