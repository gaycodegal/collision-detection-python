import sys
from multiprocessing import Process, Queue
import importlib

sandpit = "./submissions"
sys.path.append(sandpit)
CURMODULE = None
CURMODULENAME = "CURMODULE"
OPT_SILENCE = True

testFunc = None
testOpts = None

def queueGet(queue, err = None):
    try:
        return queue.get(block=False)
    except:
        return err

def timeoutImportQ(queue, hwname):
    try:
        curhw = importlib.__import__(hwname)
        curhw = importlib.reload(curhw)
        if(hwname in sys.modules):
            del sys.modules[hwname]
    except: 
        the_type, the_value, traceback = sys.exc_info()
        queue.put("%s | %s" % (str(the_type), str(the_value)))
    queue.put("done")

def timeoutImport():
    queue = Queue()
    p = Process(target=timeoutImportQ, args=(queue, CURMODULENAME))
    p.start()
    p.join(1)
    result = None
    if p.is_alive():
        recordedErrors.append("IMPORT TIMEOUT")
        p.terminate()
    else:
        result = queueGet(queue, None)
        if result == "done":
            result = importlib.__import__(CURMODULENAME)
            result = importlib.reload(result)
        elif result != None:
            recordedErrors.append(result)
            result = None
    return result
        
def getCurMod():
    return CURMODULE

def getCurModName():
    return CURMODULENAME

def importAttempt():
    global CURMODULE
    try:
        
        CURMODULE = timeoutImport()#importlib.__import__(CURMODULENAME)
        if CURMODULE == 1:
            print("HI")
            raise Exception("NOGO")
        #CURMODULE = importlib.reload(CURMODULE)
        return True
    except:
        the_type, the_value, traceback = sys.exc_info()
        printLevel(2, "File Fatal")
        printLevel(2, the_type)
        printLevel(2, the_value)
        return False

def closeAttempt():
    global CURMODULE
    if(CURMODULENAME in sys.modules):
        del sys.modules[CURMODULENAME]
        CURMODULE = None
                            
Q_DONE, Q_ERR, Q_PTS, Q_EMES = range(4)

def beginTests(tester, opts = {}):
    global testFunc, testOpts, CURMODULENAME, OPT_SILENCE
    CURMODULENAME = opts["filename"]
    OPT_SILENCE = opts["filename"]
    
    testFunc = tester
    testOpts = opts
    execTests()

class DontPrint(object):
    def write(*args): pass
    def flush(*args): pass
    
OLD_STD = None
def execTests():
    global OLD_STD
    OLD_STD = sys.stdout
    dp = DontPrint()
    if OPT_SILENCE:
        sys.stdout = dp

    if(not importAttempt()):
        return False
    try:
        testFunc()
    except:
        pass
    
    closeAttempt()
    sys.stdout = OLD_STD
    return False
    
