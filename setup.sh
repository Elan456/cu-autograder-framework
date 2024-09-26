#!/usr/bin/env bash

# python is used to run autograder scripts
apt-get install -y python3 python3-pip python3-dev 
 
# gdb can be used to debug over ssh
apt-get install -y gdb

# Installs some English dictionaries 
# These are needed for the "words" file to exist 
# apt-get install -y wamerican wbritish

pip3 install -r /autograder/source/requirements.txt

# Locking down parts of the Autograder to the student user

# Creating a student user who will have minimal permissions 
adduser student --no-create-home --disabled-password --gecos ""
chmod o= /autograder/source/tests/*  # So they can't see the test cases

# This gives them access to everything in the source directory
# However, this is being ran before all the testing scripts are copied in, so 
# they still won't be able to access them. 
chmod go=rwx /autograder/source  # So they can create files when compiling

# create temp file to download harness to
TMP_HARNESS="$(mktemp)"
curl 'https://s3-us-west-2.amazonaws.com/gradescope-static-assets/autograder/python3/harness.py' -o "$TMP_HARNESS"

# find line number of run_autograder function
line_num="$(grep -n 'def run_autograder' "$TMP_HARNESS" | cut -f1 -d:)"
# store checksum for run_autograder script
checksum="$(sha256sum /autograder/run_autograder)"

# add checksum checking to harness script
{
	head -n "$line_num" "$TMP_HARNESS"
	echo \
"        if os.system('echo \"$checksum\" | sha256sum -c') != 0:
            result = {'score': -100, 'output': 'Autograder is not allowed to be overwritten!'}
            results_path = os.path.join(self.results_path, 'results.json')
            with open(results_path, 'w') as f:
                json.dump(result, f)
            self.elapsed_time = 0
            self.exit_status = 0
            return"
	tail -n "+$((line_num + 1))" "$TMP_HARNESS"
} > /autograder/harness.py

# delete temp file
rm -f "$TMP_HARNESS"
