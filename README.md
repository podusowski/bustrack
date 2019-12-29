**butrack** is an attempt of using city's public data to analyze how traffic organization changes affect the public transportation system.


Recording
=========
First thing to do is to record the traffic. This can be done using `record` command like this:

    ./bustrack.py record --line 132 > 132.bustrack

Gathered data will be saved in `132.bustrack`


Segments
========
After you gather some data, you can do some analysis. One of them is extracting segments:

    ./bustrack.py segment 51.11208,17.02068 51.11299,17.01281 51.11317,17.00783 51.11190,17.00013 < 132.bustrack

This will find all trips through sample segment (_pl. Jana Pawła II -> Młodych Techników -> pl. Strzegomski -> Śrubowa_).

In result you should get something like this:

    ./bustrack.py segment `cat srubowa_pl-jana-pawla-ii.segment` < mpk_132.bustrack 
    2019-12-28 21:32:41 - 2019-12-28 21:38:30, duration: 0:05:49
    2019-12-28 21:02:03 - 2019-12-28 21:06:51, duration: 0:04:48

Which are times that it took bus to travel this segment.
    

Some boring, developer related stuff
====================================
Format that **butrack** uses is something similar to the `;` separated CSV except for some extensions. Lines starting with `#` are comments and `$` character starts a control line which describes columns that follow. See the example to get better grasp of it:

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