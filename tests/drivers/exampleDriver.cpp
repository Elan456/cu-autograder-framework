#include "studentCode.h"
#include <iostream>
#include <stdio.h>

using namespace std;

// Outputs if the case failed or passed
// e.g.
// Case myTest pass
void caseOutput(char* name, bool pass){
  printf("Case %s ", name);
  if (pass){
    printf("pass\n");
  } else {
    printf("fail\n");
  }
}



int main (){
  // Test 1
  caseOutput("3+3=6", studentAdd(3,3)=6);

  // Test 2
  caseOutput("1+8=9", studentAdd(1,8)=9);

  // Test 3
  caseOutput("100+500=600", studentAdd(100,500)=600);


  // Outputting a note that the all the test finished
  // If this case isn't detected in stdout, then either a
  // segmentation fault or infinite loop has occurred from the earlier function
  // calls
  caseOutput("finished", true);
}