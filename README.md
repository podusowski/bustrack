**butrack** is an attempt of using city's public data to analyze how traffic organization changes affect the public transportation system.


Recording
=========
First thing to do is to record the traffic. This can be done using `record` command like this:

    ./bustrack.py record --line 132


Data format
===========
Format that **butrack** uses for its thing is something similar to the `;` separated CSV, except for some extensions. Lines starting with `#` are comments and `$` character starts a control line which describes columns that follow. See the example to get better grasp of it:

    $ name;age
    Jan;42
    Stanisław;72

There can more than one control lines and it will simply means that new set columns should be expected from now on:

    $ name;age
    Jan;42
    Stanisław;72
    $ name;birthdate
    Franciszek;10-01-1999

This way, some degree of the compatibility can be kept in the future.