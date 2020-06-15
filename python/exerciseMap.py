"""
Exercise map for end-of-chapter problems from 5th edition International to STEA.

Where
-----
key   : sea  chapter _ problem location
value : stea chapter _ problem location

Integer values will be converted to 0-left-padded string when appropriate.
Assign '0' to an exercise to exclude it from STEA.

Example
-------
EXERCISE_MAP["sea-08-01"] = 2
EXERCISE_MAP["sea-14-03"] = 0  # exercise 14.03 will not be included in STEA
"""

EXERCISE_MAP = {}
EXERCISE_MAP["sea-08-02"] = 3

