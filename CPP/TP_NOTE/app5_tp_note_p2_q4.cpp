/**
* APP5 IIM
 * GUILLEMONT Vladimir
 * DUAULT Gaston
 * LACZKOWSKI Lorenzo
 */

#include <array>
#include <iostream>
#include <ostream>

/*
ETAPE 4 - SIMPLIFICATION
  A partir de C++20, n'importe quelle structure constexpr peut servir
  de parametres template.

  Définissez une structure spec contenant un tableau de 7 entiers et les opérations et
  constrcuteurs que vous jugerez nécessaire et implémentez dans un deuxieme fichier la
  totalité des opérations et types précédent en partant du principe que unit devient

  template<typename T, spec D> struct unit;
*/

struct spec {
    std::array<int, 7> dim;

    constexpr spec(): dim{0, 0, 0, 0, 0, 0, 0} {
    }

    constexpr explicit spec(const std::array<int, 7> &v) : dim(v) {
    }

    constexpr spec(const int mass, const int time, const int length, const int temperature, const int current,
                   const int mol, const int luminance)
        : dim{mass, time, length, temperature, current, mol, luminance} {
    }

    constexpr auto operator+(const spec &s) const {
        std::array<int, 7> result{};
        for (std::size_t i = 0; i < 7; ++i) {
            result[i] = dim[i] + s.dim[i];
        }
        return spec(result);
    }

    constexpr auto operator-(const spec &s) const {
        std::array<int, 7> result{};
        for (std::size_t i = 0; i < 7; ++i) {
            result[i] = dim[i] - s.dim[i];
        }
        return spec(result);
    }

    constexpr bool operator==(const spec &other) const {
        return dim == other.dim;
    }
};

template<typename T, spec D>
struct unit {
    T value;

    constexpr explicit unit(T v) : value(v) {
    }

    // for tests purposes
    friend std::ostream &operator<<(std::ostream &os, const unit &u) {
        static constexpr const char *unit_symbols[7] = {"kg", "s", "m", "K", "A", "mol", "cd"};

        os << u.value << " ";
        bool first = true;

        for (size_t i = 0; i < 7; ++i) {
            if (D.dim[i] != 0) {
                if (!first) os << " ";
                first = false;

                os << unit_symbols[i];
                if (D.dim[i] != 1) {
                    os << "^" << D.dim[i];
                }
            }
        }
        return os;
    }
};

template<typename T, spec D>
constexpr auto operator+(unit<T, D> const &u1, unit<T, D> const &u2) {
    return unit<T, D>{u1.value + u2.value};
}

template<typename T, spec D>
constexpr auto operator-(unit<T, D> const &u1, unit<T, D> const &u2) {
    return unit<T, D>{u1.value - u2.value};
}

template<typename T, spec D1, spec D2>
constexpr auto operator*(unit<T, D1> const &u1, unit<T, D2> const &u2) {
    return unit<T, D1 + D2>{u1.value * u2.value};
}

template<typename T, spec D1, spec D2>
constexpr auto operator/(unit<T, D1> const &u1, unit<T, D2> const &u2) {
    return unit<T, D1 - D2>{u1.value / u2.value};
}

constexpr spec mass_spec{1, 0, 0, 0, 0, 0, 0};
constexpr spec length_spec{0, 0, 1, 0, 0, 0, 0};
constexpr spec time_spec{0, 1, 0, 0, 0, 0, 0};
constexpr spec speed_spec{0, -1, 1, 0, 0, 0, 0};
constexpr spec newton_spec{1, -2, 1, 0, 0, 0, 0};
constexpr spec energy_spec{1, -2, 2, 0, 0, 0, 0};
constexpr spec resistance_spec{1, -3, 2, 0, -2, 0, 0};
constexpr spec catalyse_spec{0, -1, 0, 0, 0, 1, 0};
constexpr spec induction_spec{1, -2, 0, 0, -1, 0, 0};

template<typename T>
using mass = unit<T, mass_spec>;

template<typename T>
using length = unit<T, length_spec>;

template<typename T>
using speed = unit<T, speed_spec>;

template<typename T>
using newton = unit<T, newton_spec>;

template<typename T>
using energy = unit<T, energy_spec>;

template<typename T>
using resistance = unit<T, resistance_spec>;

template<typename T>
using catalyse = unit<T, catalyse_spec>;

template<typename T>
using induction = unit<T, induction_spec>;

int main() {
    // Test units
    std::cout << "======Tests units=======" << std::endl;

    constexpr mass<int> m{1};
    std::cout << m << std::endl;

    constexpr length<float> l{1.7};
    std::cout << l << std::endl;

    constexpr speed<double> s{3};
    std::cout << s << std::endl;

    constexpr newton<double> n{9};
    std::cout << n << std::endl;

    constexpr energy<int> e{1000};
    std::cout << e << std::endl;

    constexpr resistance<uint> r{120};
    std::cout << r << std::endl;

    constexpr catalyse<double> c{30.67};
    std::cout << c << std::endl;

    constexpr induction<int> i{3};
    std::cout << i << std::endl;

    // Test operations
    std::cout << "======Tests operations=======" << std::endl;

    constexpr auto total_mass = m + m;
    static_assert(total_mass.value == 2);
    std::cout << total_mass << std::endl;

    constexpr resistance<unsigned int> r2{80};
    constexpr auto resist = r - r2;
    static_assert(resist.value == 40);
    std::cout << resist << std::endl;

    constexpr auto combined = m * i;
    static_assert(combined.value == 3);
    std::cout << combined << std::endl;

    constexpr auto derived = n / s;
    static_assert(derived.value == 3);
    std::cout << derived << std::endl;

    return 0;
}
