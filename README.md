# label

Labels file with json header that can be understood by human/machine and applied to local rules.

t.txt file is the test sample file
t.txt.mclf is the output file

.mclf stands for multi-compartment labeled file

## Usage
Current usage:

File name and script need to be in the same location.

Change the FILE attribute towards the bottom of the file you'd like to be labeled.

Run ``python3 labeler.py``

Two additional files should be created: ``$YOURFILE.mclf`` and ``test_$YOURFILE``

``test_$YOURFILE`` and ``$YOURFILE`` should be the same and be md5 identical.
