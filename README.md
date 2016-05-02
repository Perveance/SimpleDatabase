Simple database

Data Commands

Database should accept the following commands:
  - SET name value – Sets the variable name to the value value. Neither variable names nor values will contain spaces.
  - GET name – Prints out the value of the variable name, or NULL if that variable is not set.
  - UNSET name – Unsets the variable name, making it just like that variable was never set.
  - NUMEQUALTO value – Prints out the number of variables that are currently set to value. If no variables equal that value, prints 0.
  - END – Exit the program.
