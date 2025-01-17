#include <iostream>

#import "Tracer.hpp"

int main() {
    Tracer tracer(__FUNCTION__);
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
