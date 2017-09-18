To turn in homework 2, create files (and subdirectories if needed) in
this directory, add and commit those files to your cloned repository,
and push your commit to your bare repository on GitHub.

Add any general notes or instructions for the TAs to this README file.
The TAs will read this file before evaluating your work.

---
External resource:

checkInteger(parameter) method is cited from https://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
---
GET vs POST request:

As written on W3School website (https://www.w3schools.com/tags/ref_httpmethods.asp),
GET is for requesting data from a specified resource;
while, POST is for submitting data to be processed to a specified resource

On this application, I used POST method instead of GET because the main function of this application is
the user can submit some data of numbers and operators, send it to the web server to be processed,
and get the result from the process (in this case is calculation process).

Another reason is because POST does not display the data input in the URL.
Even though my application have a validation function to ensure that the client request only contain a properly formed data,
using POST method can prevent malformed data from the URL going to the application.

---
Note for "Divide by Zero" case:

When the user attempts divide by zero input, this calculator application will reset all of the state as the first time the user open the app.
Therefore, when the users submit a number after getting error message, it will be like they submit and they can continue with the new calculation.
If the users submit an operator after getting error message, it will calculate the number after the operator with zero.

For example:
1)
input
9 | / | 0 | -     | 6 | - | 3 | =

result
9 | 9 | 0 | error | 6 | 6 | 3 | 3

2)
input
9 | / | 0 | -     | - | 6 | =

result
9 | 9 | 0 | error | 0 | 6 | -6


The calculator on iphone acts differently because when it gets an error message,
it stores error/undefined as the first operand, then it calculates the error value with the next operand
and the result will be error too.