**butrack** is an attempt of using city's public data to analyze how traffic organization changes affect the public transportation system.


Recording
=========
First thing to do is to record the traffic. This can be done using `record` command like this:

    ./bustrack.py record --line 132


Data format
===========
Format that **butrack** uses for its thing is something similar to the `;` separated CSV, except for some extensions. Lines starting with `#` are comments. `$` character starts a control line which describes following columns, for example:

    $ name;age
    Jan;42
    Stanisław;72
    