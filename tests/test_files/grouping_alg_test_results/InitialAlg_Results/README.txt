S3, S5, and S9 all appeared to be the same raw data, hence only testing for one of them.
Same for S6 and S7.

Adding "_mod" to the raw data (e.g., S1_mod_Anon.csv) indicates that there was at least
    one user in the dataset that left their availability blank (did not select at least
    one available timeslot). In these modified versions, those users are updated to
    have "complete" availability (if you don't fill it out, then you are assumed to
    be available for all slots).  We will likely update our program to make this
    change during the data loading operation, so it seemd like a reasonable thing
    to do and test here.

Seperately, the S7 dataset was found to have all of the timeslot columns duplicated, with
    the second set containing different values than the first, and 12 users having no
    availability in the second, whereas 0 have no availability in the first set. In this
    "corrected" version, the second (duplicate) set of availability columns are deleted.

The difference between "origAlg" and "modAlg1" is that the original algorithm started each
    full pass by sorting the users from most dislikes to least prior to starting to build
    the groups, with the rationale that the more disliked users are harder to group
    and should therefore be handled first.
    
    Modified algorithm 1, on the other hand, simply starts each pass by randomizing the
    order of the users, and therefore the order in which they are added to the groups (as
    the first step of the algorithm).
 
