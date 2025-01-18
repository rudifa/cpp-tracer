#include <iostream>

#include "bank-demo.hpp"
#include "tracer.hpp"

// class Aclass
// {
//    public:
//     void aaa()
//     {
//         TRACE;
//         // std::cout << "In aaa()" << std::endl;
//         bbb();
//     }

//     void bbb()
//     {
//         TRACE;
//         // std::cout << "In bbb()" << std::endl;
//         ccc();
//     }

//     void ccc()
//     {
//         TRACE;
//         // std::cout << "In ccc()" << std::endl;
//         // This method doesn't call any other method to avoid infinite
//         recursion
//     }
// };

int main()
{
    TRACE;

    std::cout << "Hello, World!" << std::endl;

    bank_demo();

    return 0;
}
