/**
* APP5 IIM
 * GUILLEMONT Vladimir
 * DUAULT Gaston
 * LACZKOWSKI Lorenzo
 */

#include <iostream>
#include <utility>

/*
Le Système international d'unités (abrégé en SI), inspiré du 
système métrique, est le système d'unités le plus largement 
employé au monde.

Le Système international comporte sept unités de base, 
destinées à mesurer des grandeurs physiques indépendantes
 et possédant chacune un symbole :

  + La masse, mesurée en kilogramme (kg).
  + Le temps, mesuré en second (s).
  + La longueur, mesuré en mètre (m).
  + La température, mesurée en kelvin (K).
  + L'intensité électrique, mesurée en ampère (A).
  + La quantité de matière, mesurée en mole   (mol).
  + L'intensité lumineuse, mesurée en candela  (cd). 

A partir de ces unités de bases, il est possible de construire 
des unités dérivées. Par exemple : 

  + La frequence, exprimée en s^-1
  + La vitesse, exprimée en m.s^-1
  + L'energie, exprimée en kg.m^2.s^−2 

On remarque que ses unités dérivées sont toutes des produits de 
puissance d'unité de base.

On se propose d'implémenter un systeme permettant de calculer des
grandeurs avec des unités en utilisant le type des objets unités
pour empecher des erreurs comme kg + m.
*/

/*
  ETAPE 1 - STRUCTURE UNIT

  Ecrivez une structure unit qui prend en parametre template un type T
  et 7 entiers, chacune représentant une unité de base. Vous les
  ordonnerez de façon à suivre l'ordre de la liste donnée plus haut.

  Cette structure contient une valeur de type T.
*/

template<typename T, int Mass, int Time, int Length, int Temperature, int Current, int Mol, int Luminosity>
struct unit {
    T value;

    constexpr explicit unit(T v) : value(v) {
    }

    // Useful for debug
    friend std::ostream &operator<<(std::ostream &os, const unit &u) {
        os << u.value << " ";
        if constexpr (Mass != 0) os << "kg^" << Mass << " ";
        if constexpr (Time != 0) os << "s^" << Time << " ";
        if constexpr (Length != 0) os << "m^" << Length << " ";
        if constexpr (Temperature != 0) os << "K^" << Temperature << " ";
        if constexpr (Current != 0) os << "A^" << Current << " ";
        if constexpr (Mol != 0) os << "mol^" << Mol << " ";
        if constexpr (Luminosity != 0) os << "cd^" << Luminosity << " ";
        return os;
    }
};

/*
  ETAPE 2 - UNITES ET UNITES DERIVEES
  En utilisant le modele ci dessous, définissez des types
  representant les grandeurs demandées.

  Indice : https://fr.wikipedia.org/wiki/Syst%C3%A8me_international_d%27unit%C3%A9s#Unit%C3%A9s_d%C3%A9riv%C3%A9es
*/

// Masse : kg
template<typename T>
using mass = unit<T, 1, 0, 0, 0, 0, 0, 0>;

// Longeur : m
template<typename T>
using length = unit<T, 0, 0, 1, 0, 0, 0, 0>;

// Vitesse m.s-1
template<typename T>
using speed = unit<T, 0, -1, 1, 0, 0, 0, 0>;

// Force exprimée en Newton
template<typename T>
using newton = unit<T, 1, -2, 1, 0, 0, 0, 0>;

// conductance électrique
template<typename T>
using siemens = unit<T, -1, 3, -2, 0, 2, 0, 0>;

// Create other units for test
template<typename T>
using energy = unit<T, 1, -2, 2, 0, 0, 0, 0>;

template<typename T>
using resistance = unit<T, 1, -3, 2, 0, -2, 0, 0>;

template<typename T>
using catalyse = unit<T, 0, -1, 0, 0, 0, 1, 0>;

template<typename T>
using induction = unit<T, 1, -2, 0, 0, -1, 0, 0>;

/*
  ETAPE 3 - OPERATIONS

  Ecrivez les operateurs +,-,* et / entre deux unités
  du même type mais avec des unités cohérentes.

  On peut multipliez ou divisé du temps par une masse mais
  on ne peut pas ajouter des Kelvin à des metres.
*/

template<typename T, int Mass, int Time, int Length, int Temperature, int Current, int Mol, int Luminosity>
constexpr auto operator+(unit<T, Mass, Time, Length, Temperature, Current, Mol, Luminosity> const &u1,
                unit<T, Mass, Time, Length, Temperature, Current, Mol, Luminosity> const &u2) {
    return unit<T, Mass, Time, Length, Temperature, Current, Mol, Luminosity>{u1.value + u2.value};
}

template<typename T, int Mass, int Time, int Length, int Temperature, int Current, int Mol, int Luminosity>
constexpr auto operator-(unit<T, Mass, Time, Length, Temperature, Current, Mol, Luminosity> const &u1,
                unit<T, Mass, Time, Length, Temperature, Current, Mol, Luminosity> const &u2) {
    return unit<T, Mass, Time, Length, Temperature, Current, Mol, Luminosity>{u1.value - u2.value};
}

template<typename T, int Mass1, int Time1, int Length1, int Temperature1, int Current1, int Mol1, int Luminosity1,
    int Mass2, int Time2, int Length2, int Temperature2, int Current2, int Mol2, int Luminosity2>
constexpr auto operator*(unit<T, Mass1, Time1, Length1, Temperature1, Current1, Mol1, Luminosity1> const &u1,
                unit<T, Mass2, Time2, Length2, Temperature2, Current2, Mol2, Luminosity2> const &u2) {
    return unit<T, Mass1 + Mass2, Time1 + Time2, Length1 + Length2, Temperature1 + Temperature2, Current1 + Current2,
        Mol1 + Mol2, Luminosity1 + Luminosity2>{u1.value * u2.value};
}

template<typename T, int Mass1, int Time1, int Length1, int Temperature1, int Current1, int Mol1, int Luminosity1,
    int Mass2, int Time2, int Length2, int Temperature2, int Current2, int Mol2, int Luminosity2>
constexpr auto operator/(unit<T, Mass1, Time1, Length1, Temperature1, Current1, Mol1, Luminosity1> const &u1,
                unit<T, Mass2, Time2, Length2, Temperature2, Current2, Mol2, Luminosity2> const &u2) {
    return unit<T, Mass1 - Mass2, Time1 - Time2, Length1 - Length2, Temperature1 - Temperature2, Current1 - Current2,
        Mol1 - Mol2, Luminosity1 - Luminosity2>{u1.value / u2.value};
}

/*
  ETAPE 4 - SIMPLIFICATION
  A partir de C++20, n'importe quelle structure constexpr peut servir
  de parametres template.

  Définissez une structure spec contenant un tableau de 7 entiers et les opérations et
  constrcuteurs que vous jugerez nécessaire et implémentez dans un deuxieme fichier la
  totalité des opérations et types précédent en partant du principe que unit devient

  template<typename T, spec D> struct unit;
*/

int main() {
    // POUR CHAQUE ETAPE, ECRIVEZ LES TESTS QUE VOUS JUGEREZ SUFFISANT

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

    constexpr siemens<short> si{256};
    std::cout << si << std::endl;

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

    constexpr auto mass = m + m;
    static_assert(mass.value == 2);
    std::cout << mass << std::endl;

    // constexpr auto wtf = m + l; // Should not compile if uncommented

    constexpr resistance<uint> r2{80};
    constexpr auto resist = r - r2;
    static_assert(resist.value == 40);
    std::cout << resist << std::endl;

    // constexpr auto wtf2 = r - c - r2; // Should not compile if uncommented

    constexpr auto dont_know1 = m * i;
    static_assert(dont_know1.value == 3);
    std::cout << dont_know1 << std::endl;

    constexpr auto dont_know2 = n / s;
    static_assert(dont_know2.value == 3);
    std::cout << dont_know2 << std::endl;


}
