import ctypes
from ctypes import c_char_p, c_size_t, c_uint32, POINTER, c_bool, byref
import time
import os
import shutil
import inspect
import random
import string

# Load the DLL
dll = ctypes.CDLL(r'C:\Users\Lejma\Downloads\HID QA HomeworkV2\bin\windows\hash.dll')

# Define argument and return types for each function
dll.HashInit.restype = c_uint32
dll.HashTerminate.restype = c_uint32
dll.HashDirectory.argtypes = (c_char_p, POINTER(c_size_t))
dll.HashDirectory.restype = c_uint32
dll.HashStatus.argtypes = (c_size_t, POINTER(c_bool))
dll.HashStatus.restype = c_uint32
dll.HashReadNextLogLine.argtypes = [POINTER(c_char_p)]
dll.HashReadNextLogLine.restype = c_uint32
dll.HashFree.argtypes = [c_char_p]
dll.HashFree.restype = None

# helper functions
def thisTestName():
    return inspect.currentframe().f_back.f_code.co_name

def createRandomFile(directoryPath): 
    random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.txt'
    if not os.path.exists(os.path.join(directoryPath, random_filename)):
        with open(os.path.join(directoryPath, random_filename), "w") as file:
            file.write(f"some content for file {random_filename}")
        time.sleep(1)
        return random_filename
    else: 
        print(f"path {directoryPath}\{random_filename} already exists")

# TESTS
# test set 1 - HashInit
def HashInitOKTest():
    print(f"{thisTestName()} begins")
    error_code = dll.HashInit()
    if error_code == 0: 
        print(f"{thisTestName()} PASSED")
    else:
        print(f"{thisTestName()} FAILED, error code expected 0, but was: {error_code}")
    # silent cleanup
    dll.HashTerminate()
    print(f"{thisTestName()} ends")

def HashInitAlreadyInitializedTest():
    print(f"{thisTestName()} begins")
    error_code = dll.HashInit()
    if error_code == 0: 
        error_code = dll.HashInit()
        if error_code == 8: 
            print(f"{thisTestName()} PASSED")
        else:
            print(f"{thisTestName()} FAILED, error code expected 8, but was: {error_code}")
    else: 
        print(f"{thisTestName()} FAILED on prerequisite")
    # silent cleanup
    #dll.HashTerminate()
    print(f"{thisTestName()} ends")

# test set 2 - HashTerminate
def HashTerminateOKTest():
    print(f"{thisTestName()} begins")
    error_code = dll.HashInit()
    if error_code == 0: 
        error_code = dll.HashTerminate()
        if error_code == 0: 
            print(f"{thisTestName()} PASSED")
        else:
            print(f"{thisTestName()} FAILED, error code expected 0, but was: {error_code}")
    else: 
        print(f"{thisTestName()} FAILED on prerequisite")
    print(f"{thisTestName()} ends")

def HashTerminateNotInitializedTest():
    print(f"{thisTestName()} begins")
    error_code = dll.HashTerminate()
    if error_code == 7: # i know, this is pretty weird
        error_code = dll.HashTerminate()
        if error_code == 7: 
            print(f"{thisTestName()} PASSED")
        else:
            print(f"{thisTestName()} FAILED, error code expected 7, but was: {error_code}")
    else: 
        print(f"{thisTestName()} FAILED on prerequisite")
    print(f"{thisTestName()} ends")

# test set 3 - HashDirectory
def HashDirectoryOKTest():
    print(f"{thisTestName()} begins")
    test_dir = r".\testdir1"
    error_code = dll.HashInit()
    if error_code != 0:
        print(f"{thisTestName()} FAILED on prerequisite - HashInit, error code: {error_code}")
        return
    # here im really assuming such basic operation as dir and file creation simply passes without issues
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    #createRandomFile(test_dir)
    with open(os.path.join(test_dir, "abc.txt"), "w") as file:
        file.write(f"some content for file")
    operation_id = c_size_t()
    error_code = dll.HashDirectory(test_dir.encode('utf-8'), byref(operation_id))
    if error_code == 0: 
        print(f"{thisTestName()} PASSED")
    else:
        print(f"{thisTestName()} FAILED, error code expected 0, but was: {error_code}")
    # silent cleanup
    time.sleep(5) # this will need to be replaced by wait for HashDirectory to finish doing what its doing
    dll.HashTerminate() # test is hanging, no idea why, but commenting out this fixes it
    shutil.rmtree(test_dir)
    print(f"{thisTestName()} ends")

def HashDirectoryArgumentNullDirectoryTest():
    print(f"{thisTestName()} begins")
    test_dir = None # null intended
    error_code = dll.HashInit()
    if error_code != 0:
        print(f"{thisTestName()} FAILED on prerequisite - HashInit, error code: {error_code}")
        return
    operation_id = c_size_t()
    error_code = dll.HashDirectory(test_dir, byref(operation_id))
    if error_code == 6: 
        print(f"{thisTestName()} PASSED")
    else:
        print(f"{thisTestName()} FAILED, error code expected 6, but was: {error_code}")
    # silent cleanup
    time.sleep(5) # this will need to be replaced by wait for HashDirectory to finish doing what its doing
    dll.HashTerminate()
    print(f"{thisTestName()} ends")

# test set 4 - HashReadNextLogLine
def HashReadNextLogLineTest():
    print(f"{thisTestName()} begins")
    test_dir = r".\testdir2"
    error_code = dll.HashInit()

    if error_code != 0:
        print(f"{thisTestName()} FAILED on prerequisite - HashInit, error code: {error_code}")
        return
    # here im really assuming such basic operation as dir and file creation simply passes without issues
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)

    #file1 = createRandomFile(test_dir)
    #file2 = createRandomFile(test_dir)
    with open(os.path.join(test_dir, "xyz.txt"), "w") as file1:
        file1.write(f"some content for file")

    with open(os.path.join(test_dir, "def.txt"), "w") as file2:
        file2.write(f"some content for file")

    operation_id = c_size_t()
    error_code = dll.HashDirectory(test_dir.encode('utf-8'), byref(operation_id))
    if error_code != 0:
        print(f"FAILED on prerequisite - HashDirectory, error code: {error_code}")
        return

    is_running = c_bool(True)

    while is_running.value:
        error_code = dll.HashStatus(operation_id, byref(is_running))
        if error_code != 0:
            print(f"FAILED on prerequisite - HashStatus, error code: {error_code}")
            return
        if not is_running.value:
            break
    hash_log_entry = c_char_p()
    hash_log_entries = []
    counter = 1
    while True:
        print(f"iteration no.: {counter}")
        error_code = dll.HashReadNextLogLine(byref(hash_log_entry))
        if error_code == 4: # log empty, nothing to read
            break
        elif error_code == 0:
            log_entry = hash_log_entry.value.decode('utf-8')
            print(f"Hash log entry: {log_entry}")
            hash_log_entries.append(log_entry)
        else:
            print(f"FAILED reading log, error code: {error_code}")
            return
        counter = counter + 1
    # after the above code is finished i can check the hash_log_entries var and evaluate
    # whether the data returned are as expected, such as format of log entry, operation id being unique
    # filename displayed, hash value (in this case would be better to copy known files rather than create random ones as i did)
    # silent cleanup
    shutil.rmtree(test_dir)
    time.sleep(5) # this will need to be replaced by wait for HashDirectory to finish doing what its doing
    dll.HashTerminate()
    print(f"{thisTestName()} ends")



# TESTS
# test set 1 - HashInit
HashInitOKTest()
HashInitAlreadyInitializedTest()
# test set 2 - HashTerminate
HashTerminateOKTest()
HashTerminateNotInitializedTest()
# test set 3 - HashReadNextLogLine
HashDirectoryOKTest()
HashDirectoryArgumentNullDirectoryTest()
# test set 4 - HashReadNextLogLine
HashReadNextLogLineTest()
