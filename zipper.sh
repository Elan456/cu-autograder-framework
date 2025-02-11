# Use this to zip up the autograder 
# Run it from within the autograder directory

# SET NAME BELOW 
name="autograder"

zip -r ../$name.zip . -x ".*" -x "example_sample_code/*" -x "*__pycache__/*" -x "*.zip"
