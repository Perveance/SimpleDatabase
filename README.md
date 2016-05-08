Simple database

Data Commands

Database accepts the following commands:
  - SET name value – Sets the variable name to the value value. Neither variable names nor values will contain spaces.
  - GET name – Prints out the value of the variable name, or NULL if that variable is not set.
  - UNSET name – Unsets the variable name, making it just like that variable was never set.
  - NUMEQUALTO value – Prints out the number of variables that are currently set to value. If no variables equal that value, prints 0.
  - END – Exit the program.

Transaction Commands

In addition to the above data commands, database also supports transactions by also implementing these commands:
  - BEGIN – Open a new transaction block. Transaction blocks can be nested; a BEGIN can be issued inside of an existing block.
  - ROLLBACK – Undo all of the commands issued in the most recent transaction block, and close the block. Prints nothing if successful, or prints NO TRANSACTION if no transaction is in progress.
  - COMMIT – Closes all open transaction blocks, permanently applying the changes made in them. Prints nothing if successful, or print NO TRANSACTION if no transaction is in progress.

Any data command that is run outside of a transaction block commits immediately. 
Here are some example command sequences:

# python myDB.py 
GET a
NULL
SET a 10
GET a
10
NUMEQUALTO 10
1
BEGIN
UNSET a
GET a
NULL
ROLLBACK
GET a
10
BEGIN
SET b 15
BEGIN SET b 20
GET b
15
ROLLBACK
GET b
15
COMMIT
GET b
15
END
