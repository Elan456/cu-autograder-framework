#include <iostream>
#include <string>
#include <fstream>
#include "studentFuncs.h"

using namespace std; 


void no_file_mode(){
    cout << "Enter first number or q to quit: ";
    string input;
    cin >> input;

    if (input == "q") {
        cout << "Exiting program" << endl;
        return;
    }

    int num1 = stoi(input);

    cout << "Enter second number: ";
    int num2;
    cin >> num2;

    int op;
    cout << "Enter operation [1: add, 2: subtract, 3: multiply, 4: divide]: ";
    cin >> op;

    switch (op) {
        case 1:
            cout << "Result: " << studentAdd(num1, num2) << endl;
            break;
        case 2:
            cout << "Result: " << studentSubtract(num1, num2) << endl;
            break;
        case 3:
            cout << "Result: " << studentMultiply(num1, num2) << endl;
            break;
        case 4:
            cout << "Result: " << studentInfiniteDivide(num1, num2) << endl;
            break;
        default:
            cout << "Invalid operation" << endl;
            break;
    }
}

void file_mode(string file_name) {
    cout << "File mode" << endl;
    cout << "File name: " << file_name << endl;

    // Opening file
    ifstream file(file_name);

    if (!file.is_open()) {
        cout << "Error opening file" << endl;
        return;
    }

    // Lines are in groups of 3 
    // First line is the operation [add, subtract, multiply, divide]
    // Second line is the first number
    // Third line is the second number

    // The result must be written to output.txt
    FILE *output = fopen("output.txt", "w");

    string operation;
    int num1;
    int num2;

    while (file >> operation >> num1 >> num2) {
        cout << "Operation: " << operation << endl;
        cout << "Num1: " << num1 << endl;
        cout << "Num2: " << num2 << endl;

        int result = 0;

        if (operation == "add") {
            result = studentAdd(num1, num2);
        } else if (operation == "subtract") {
            result = studentSubtract(num1, num2);
        } else if (operation == "multiply") {
            result = studentMultiply(num1, num2);
        } else if (operation == "divide") {
            result = studentDivide(num1, num2);
        } else {
            cout << "Invalid operation" << endl;
            continue;
        }

        cout << "Result: " << result << endl;
        fprintf(output, "%d\n", result);
    }

    cout << "Output has been written to output.txt" << endl;
    fclose(output);
}

int main(int argc, char *argv[]) {
    cout << "Welcome to the calculator program!" << endl;
    
    // Check for -f arg to see if a file was specified

    if (argc > 1) {
        if (string(argv[1]) == "-f") {
            if (argc > 2) {
                file_mode(argv[2]);
                return 0;
            } else {
                cout << "No file name given" << endl;
                return 1;
            }
            
        }
    }

    cout << "No input file given" << endl;
    cout << "Defaulting to manual input" << endl;
    no_file_mode();
}


void say_hello() {
    cout << "Hello from studentMain.cpp" << endl;
}
