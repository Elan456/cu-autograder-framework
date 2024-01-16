#include "studentCode.h"
#include <string>
#include <iostream>

using namespace std;

// Outputs if the case failed or passed
// e.g.
// Case myTest pass
void caseOutput(string name, bool pass) {
  cout << "Case " << name << " "; 
  if (pass) {
	  cout << "pass" << endl;
  } else {
	  cout << "fail" << endl;
  }
}

// Don't put too many tests in one file
// If one causes a seg fault or infinite loop, then the rest of the tests won't
// be run
int main() {
  // Test 1
  caseOutput("3+3=6", studentAdd(3, 3) == 6);

  // Test 2
  caseOutput("1+8=9", studentAdd(1, 8) == 9);

  // Test 3
  caseOutput("100+500=600", studentAdd(100, 500) == 600);

  // Test 4
  caseOutput("1+1=2", studentAdd(1, 1) == 2);

  // Outputting a note that the all the test finished
  // If this case isn't detected in stdout, then either a
  // segmentation fault or infinite loop has occurred from the earlier function
  // calls
  caseOutput("finished", true);
}
