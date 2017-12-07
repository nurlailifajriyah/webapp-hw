Homework 6 Feedback
==================

Commit graded: 72a2039385f219d6614b4fbfd0d70b5da9c43f06

### Incremental development using Git (10/10)

### Fulfilling our specification (38/50)

-2, You should not run with `DEBUG = True` in production.

-5, Passwords, access keys, and other sensitive information should never be committed in a repository accessible by multiple people. Your code reflects that you are committing secret key.

-5, The data should be stored in a relational database that is not SQLite. SQLite is a lightweight database that can not handle production-level load. For example, SQLite does not allow for concurrent access of data, which would mean that multiple users would not be able to use your site. In your readme, you said you are using postgres, however, in your settings.py it's still sqlite.

### Responding to hw5 feedback (20/20)

---
#### Total score (68/80)
---
Graded by: Sheng Qian (sqian@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/nfajriya/blob/master/grades/homework6.md

