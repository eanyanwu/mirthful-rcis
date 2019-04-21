Work in progress....


## New to Python?

Start [here](https://docs.python.org/3/tutorial/)

Another resorce [here](https://docs.python-guide.org/)

## Using Virtual Environments

TODO


## Flask

Documentation available [here](http://flask.pocoo.org/docs/1.0/)


## Authorization:

Authorization was one of the first things designd, so it is tightly integrated into the system.

I wanted to be as flexible as possible with authorization rules. Receiving a new requirement to 'let user x view resource y' should be dead-simple. Ideally, it should be so simple, I won't have to lift a finger because there will be a UI for it. 

I opted with Access Control Lists because (a) filesystems use them and (b) the system i am building is similar to a file system in a lot ways.
Specifically, this system is about creating documents. What I want is a way to authorize who gets to view and edit what.

To do so, every api-facing 'resource' has an 'access control'. If you are familiar with unix-style acls, this will look familiar.

An access control looks like this: `owner:rw;group:r_;world:__`

This says that the owner of the resource has (r)ead and (w)rite permissions on it. Members of the groups associated with this resource only have (r)ead permissions and everyone has has no permissions at all.

To complete the picture, every api-facing resource has a list of owners and and list of groups.

The main authorization code takes these three pieces in addition to the logged in user and decides if the user should be able to perform the given action


