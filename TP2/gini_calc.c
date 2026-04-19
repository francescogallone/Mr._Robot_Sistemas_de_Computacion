#include <stdio.h>

extern int convert_and_sum(float value) {
    int int_value = (int)value; 
    int sum = int_value + 1; 
    return sum; 
}