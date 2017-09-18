To turn in homework 2, create files (and subdirectories if needed) in
this directory, add and commit those files to your cloned repository,
and push your commit to your bare repository on GitHub.

Add any general notes or instructions for the TAs to this README file.
The TAs will read this file before evaluating your work.

---
GET vs POST request

As written on W3School website (https://www.w3schools.com/tags/ref_httpmethods.asp),
GET is for requesting data from a specified resource;
while, POST is for submitting data to be processed to a specified resource

On this application, I used POST method instead of GET because the main function of this application is
the user can submit some data of numbers and operators, send it to the web server to be processed,
and get the result from the process (in this case is calculation process).

Another reason is because POST does not display the data input in the URL.
Even though my application have a validation function to ensure that the client request only contain a properly formed data,
using POST method can prevent malformed data from the URL going to the application.