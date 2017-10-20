Homework 4 Feedback
==================

Commit graded: 671d709718b06692e68f7a97ff5a71d062d1ac94

### Incremental development using Git (10/10)

### Fulfilling the grumblr specification (29.9/30)

-0, You shouldn’t be able to follow yourself

-0.1, It is impossible to find users to follow unless you know their username and enter the exact url for their profile page.

### Proper Form-based validation (14/20)

-1, You should not be able to view the login/register page when a user has already signed in.

-3, Validation for all inputs should be done with Django Forms.  In add_item you are still manually validating input.

-2, When using Django Forms, you should use the data in `form.cleaned_data` because that dictionary contains the processed inputs from the user.

### Appropriate use of web application technologies (55/60)

#### Template Inheritance and Reverse Urls (7/10)

-3, Even though you use template inheritance there is still a lot of duplication. For example, your global stream has the navbar code that can be inherited from your base file. Template inheritance allows you to cut down on repeating HTML/CSS code and improves the consistency of your web app.

-0, `<title>` tags for each page should contain a short textual description of what page the user is actually on. For instance, a login page could be title ‘Login’

#### Image upload (5/5)

#### Email Sending (5/5)

-0.1, Consider looking into check_token for checking your one time use token.

#### Basic ORM Usage (20/20)

-0, For following, it's not necessary to make a separate model for that relation unless you want to attach additional information to that relation. Instead, a better relation to use would be the [Many-to-many relationships](https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/).  

#### Advanced ORM Usage (10/10)

#### Routing and Requests (8/10)

-2, You should modularize your Django projects by using application-specific `urls.py` files in each application directory, and use your project-wide `urls.py` file to include each application's routes.

### Design

-0.1, You should consider keeping a logged in user logged in when the user's information is updated.

-0, You may want to consider breaking views.py into several files grouped by functionality

### Additional Information

---
#### Total score (109/120)
---
Graded by: Vivian Wang (vivianwa@andrew.cmu.edu)
