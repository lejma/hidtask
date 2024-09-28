just run test.py, logs status of the test into the console, below example of the run for commited version: 

HashInitOKTest begins
HashInitOKTest PASSED
HashInitOKTest ends
HashInitAlreadyInitializedTest begins
HashInitAlreadyInitializedTest FAILED, error code expected 8, but was: 0
HashInitAlreadyInitializedTest ends
HashTerminateOKTest begins
HashTerminateOKTest PASSED
HashTerminateOKTest ends
HashTerminateNotInitializedTest begins
HashTerminateNotInitializedTest PASSED
HashTerminateNotInitializedTest ends
HashDirectoryOKTest begins
HashDirectoryOKTest PASSED
HashDirectoryOKTest ends
HashDirectoryArgumentNullDirectoryTest begins
HashDirectoryArgumentNullDirectoryTest PASSED
HashDirectoryArgumentNullDirectoryTest ends
HashReadNextLogLineTest begins
iteration no.: 1
Hash log entry: 1 .\testdir1\abc.txt 3397C05D91D1EB4D2D8AC489C57FE6
iteration no.: 2
Hash log entry: 1 .\testdir2\def.txt 3397C05D91D1EB4D2D8AC489C57FE6
iteration no.: 3
Hash log entry: 1 .\testdir2\xyz.txt 3397C05D91D1EB4D2D8AC489C57FE6
iteration no.: 4
FAILED reading log, error code: 1

issues found: 
- HashInitAlreadyInitializedTest fails, test found that when init is happening twice the second one does not return already initialized error code
- HashReadNextLogLineTest - this one i did not finish, but it already shows an error when retrieving log, when end of log is reached it still returns an error regardless
another issue observed is that log entries all have oepration id 1 and not unique nor incremental
another issue observed is that, at least as per HID_QA_TestSpecification.pdf document statement, the format of “<operation id> <filename> <MD5 hash in hexadecimal notation>”, but was found out the <filename> is not displayed, instead whole path is displayed
another issue observed is when a to-be hashed directory contains a file which has czech characters in its name (such as "ý", for example file named "nový dokument.txt", it causes the hashDirectory method to be stuck forever

