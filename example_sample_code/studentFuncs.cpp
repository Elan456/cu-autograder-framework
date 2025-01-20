#include "studentFuncs.h"
#include <iostream>

int studentAdd(int a, int b) {
    return a + b;
}

int studentSubtract(int a, int b) {
    return a - b;
}

int studentMultiply(int a, int b) {
    return a * b;
}

int studentDivide(int a, int b) {
    return a / b;
}

int studentInfiniteDivide(int a, int b) {
    // Simulates a timeout infinte loop
    while (true) {
        std::cout << "Dividing " << a << " by " << b << std::endl;
    }
    return a / b; // This line will never be reached
}