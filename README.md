## Why this project?

When students move in to their room in college, they _usually_ fill out a form and list any damages they find. In some schools, the Housing staff do this for them. Either way, the school needs a way to keep track of the state of their buildings so they can charge for vandalism and conduct repair when needed. Until we have the technology to automatically scan every inch of a room in 3D, there is no getting around this process.

Although the process is inconvenient, we can make it less so. One such way is to use a custom digital form instead of a paper one. This gives the following advantages:
- With the data being recorded by a computer, you can now automate previously cumbersome tasks like compiling the list of fines, sending out emails or creating work requests to get damages repaired.
- You are no longer limited to text to discribe damages. Take a picture as well.
- No paper :tada:

## Can I try it out?

Yes! 

There is a live demo page here [ [link coming soon]() ]

If you are curious, or want to mess with the code on your local machine, here are some instructions to get you started:

1. Install [git](https://git-scm.com/), [python](https://www.python.org/downloads/) and pip. (pip usually comes bundled with python)
    - For linux users: you'll can probably get these items using your package manager.
1. Install virtualenv using the following command `pip install virtualenv`
    - virtualenv encapsualtes all the dependencies this project has in a specific folder. Once you are done trying this out, all you need is to delete that folder from you computer.
    - virtualenv is even more helpful when working with others, so check out the introduction section at this [link](https://virtualenv.pypa.io/en/latest/) if you are interested.
1. From the terminal or command line, clone this repository: `git clone https://github.com/hilarious-capital/mirthful-rcis.git`
1. Move into the directory that was created and execute: `virtualenv venv`.
1. Activate the virtualenv environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
1. Install the project dependencies: `pip install Flask pytest`
1. Start the local development server:
    - Windows: `.\flask_run.bat`
    - Mac/Linux: `./flask_run.sh`

   
    




