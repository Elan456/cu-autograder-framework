#!/usr/bin/env bash

apt-get install -y python3 python3-pip python3-dev

# Installs some English dictionaries 
# These are needed for any word-based assignments like Cipher decoding 
apt-get install -y wamerican wbritish

pip3 install -r /autograder/source/requirements.txt

# Locking down parts of the Autograder to the student user

# Creating a student user who will have minimal permissions 
adduser student --no-create-home --disabled-password --gecos ""
chmod o= /autograder/source/tests/*  # So they can't see the test cases

# This gives them access to everything in the source directory
# However, this is being ran before all the testing scripts are copied in, so 
# they still won't be able to access them. 
chmod go=rwx /autograder/source  # So they can create files when compiling
