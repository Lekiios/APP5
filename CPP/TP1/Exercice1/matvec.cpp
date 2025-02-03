#include "matvec.hpp"

#include <iostream>

int main(int, char const *[]) {

    //====== Vectors ======

    auto v = vec<int, 3>{1, 2, 3};

    std::cout << "v = [" << v[0] << ", " << v[1] << ", " << v[2] << "]" << std::endl;
    std::cout << "size of v: " << v.size() << std::endl;

    auto v2 = vec<float, 5>{3.14};

    std::cout << "v2 = [" << v2[0] << ", " << v2[1] << ", " << v2[2] << "]" << std::endl;
    std::cout << "size of v2: " << v2.size() << std::endl;

    vec<double, 2> v3;
    v3[0] = 1.0;
    v3[1] = 2.0;
    std::cout << "v3 = [" << v3[0] << ", " << v3[1] << ", " << v3[2] << "]" << std::endl;
    std::cout << "size of v3: " << v3.size() << std::endl;

    //====== Matrices ======

    auto m = mat<int, 2, 3>{1};
    std::cout << "m = [[" << m(0, 0) << ", " << m(0, 1) << ", " << m(0, 2) << "]" << std::endl << "     ["
            << m(1, 0) << ", " << m(1, 1) << ", " << m(1, 2) << "]]" << std::endl;
    std::cout << "size of m: " << m.m() << "x" << m.n() << std::endl;

    std::array<std::array<int, 2>, 3> arr = {{1, 2, 3}, {4, 5, 6}};
    auto m2 = mat<int, 2, 3>{arr};
    std::cout << "m2 = [[" << m2(0, 0) << ", " << m2(0, 1) << ", " << m2(0, 2) << "]" << std::endl << "     ["
            << m2(1, 0) << ", " << m2(1, 1) << ", " << m2(1, 2) << "]]" << std::endl;
    std::cout << "size of m: " << m2.m() << "x" << m2.n() << std::endl;


    return 0;
}
