To turn in homework 6, create files (and subdirectories if needed) in
this directory, add and commit those files to your cloned repository,
and push your commit to your bare repository on GitHub.

Add any general notes or instructions for the TAs to this README file.
The TAs will read this file before evaluating your work.

------
App's URL : https://agile-coast-49990.herokuapp.com

Sources:
- Datetime parser: https://stackoverflow.com/questions/466345/converting-string-into-datetime
- S3 Setup: https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
- Heroku Config Var: https://devcenter.heroku.com/articles/config-vars
- Sendgrid: https://sendgrid.com/docs/Integrate/Frameworks/django.html

Notes:
- This application is deployed to Heroku, using AWS S3 to store the static and media files, also PostgreSQL as the DBMS.
- The key access to the AWS S3 is stored on the Heroku. Therefore, the app cannot be run from the local server.
