#include <iostream>
#include "algorithms_templates_sujet.hpp"

// Nous n'avons pas eu le temps d'implémenter des tests exhaustifs
// Implémentez les vôtres !
int main() {
    constexpr type_list<int, float, char[19], double, char, void **> x;

    static_assert(size(x) == 6);
    static_assert(size(x + x) == 12);

    constexpr type_list<int, float> a;
    constexpr type_list<char[8], long> b;
    static_assert(size(a + b) == 4);

    static_assert(largest(x) == 19); // char[19]
    static_assert(largest(a) == 4); // float
    static_assert(largest(b) == 8); // char[8]

    all_of<int>(x);


    /*std::cout << reduce(x, []<typename T>(type_list<T> t, std::size_t i)
    { return sizeof(T) + i ;}, 0ULL) << "\n";*/
}
