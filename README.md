## About:

Version 2 of Gordon College's Online Rci System.

## Why a new version? 

_Premise 1_: The first version of the online rci form was successful and well received.  

_Premise 2_: The first version does not lend itself to maintainance or hand-off.[1]  

_Premise 3_: Gordon College's residence life program will sooner or later find the current system to be insufficient and require an update.[2]


_Conclusion_: A new version, which can be maintained by others, must be made.

[1] Obstacles to maintaining the current version of the online rci form:
- Lack of accessibility: All development is done on a virtual machine that sits on Gordon's network. A vpn is required if you are not on-campus.
- No Testing process: I think this is because we had not yet learned about the usefulness of testing in catching regressions and granting much needed peace of mind.  
- No value to student maintainers: It is tightly coupled to Gordon's database system. Working with it is not a transferable skill.

[2] A few scenarios that seem likely to me: 
- Gordon database schema changes.
- Residence life administrators start updating Jenzebar differently, which might cause problems in the code for generating rcis.
- RDs realize how restrictive and rigid the system is (I bet some of them already do) and revolt. 

