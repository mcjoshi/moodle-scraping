# moodle-scraping 
[![N|Solid](https://moodle.org/logo/moodle-logo.svg)](https://moodle.iitb.ac.in/)  Script that scraps IITB moodle and finds the occurances of a RegExp in a registered course.
>  **You must be in iitb network or use iitbVPN to run this, as moodle is not accessible outside**

 > Enter the pattern [regular expression] in quotes, as +1 is not a valid regexp, so it will not be considered as i have used re.match() which doesn't consider +1 a valid regexp. (it doesnt consider + quantifiable)

## Runnign Instructions
```sh
Input : python3 mparse.py <LDAP ID> <Password> <RegExp_to_search_in_quotes>
```

```sh
$ python3 mparse.py 173050006 12345678 "\+1"
```

Ex: "\+1" , "\+[1]", "- Om", "\- Om", "\-[ ]Om" and "Thanks" will work, but not if you give simply string "+1", because it takes regexp and matches them.

>> It further requires another input inside that is , which course you want to access out of all you have access to : [ this cannot be given as command line argument because we don't know input courses one have regisred at that time.]

### Script's step by step working: 
* accepts inputs like username password and pattern as command line argument
*  logs in to your moodle account and creates a session
* shows you list of all courses you have access in moodle
*  asks you to choose the course in which you want to search the pattern you have entered 
* it then finds link for discussion forum of that course
* find all the discussion threads for a course, shows it's count in screen 
* then for each discussion link, it iterates over all posts and counts the number of times the pattern occurs


**O/P**  : Prints the count of a pattern in complete discussion forum of a course [say CS725]

*******************************************************************************************************************************

My script searches for patterns not strings. So searching for "\+1" and "\+[1]" will give same count. So is searching for "- Om" and "\- Om" and "\-[ ]Om"
### Todos
 - Automatically configure VPN if accessing moodle from outside IITB netowrk


