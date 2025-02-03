#pragma once

#include <array>
#include <cstddef>
#include <stdexcept>

// Type vec(tor)

// Implementez vec, qui est un vecteur (au sens mathematique, pas un std::vector
// de taille dynamique). Les donnees sont stockees dans un std::array, et la
// structure fournit un operator[] (const et non-const), un constructeur par
// valeur pour initialiser toutes les valeurs (ce que ne fait pas std::array),
// et un membre size().

template<typename T, std::size_t N>
struct vec {
    std::array<T, N> data;

    //========== Constructors ==========
    explicit vec() = default;

    explicit vec(const T &value) {
        data.fill(value);
    }

    template<typename... Args,
        typename = std::enable_if_t<sizeof...(Args) == N> >
    explicit vec(Args... args) : data{{args...}} {
    }

    //========== Operators ==========

    const auto operator[](std::ptrdiff_t i) const -> T & { return data[i]; }

    auto operator[](std::ptrdiff_t i) -> T & {
        return data[i];
    }

    //========== Methods ==========

    [[nodiscard]] constexpr std::size_t size() const { return N; }
};

// Sur le meme modele, implementez mat qui est un type matrice.
// Elle doit fournir un constructeur par valeur pour initialiser le contenu,
// des membres m() et n() pour acceder aux dimensions (respectivement hauteur
// et largeur), un operator()(std::size_t, std::size_t) (const et non-const)
// pour l'acces aux elements, ainsi que deux methodes col(std::size_t) et
// row(std::size_t), qui permettent d'extraire respectivement une colonne ou une
// ligne de la matrice.

template<typename T, std::size_t M, std::size_t N>
struct mat {
    std::array<T, N * M> data;

    //========== Constructors ==========

    mat() = default;

    explicit mat(const T &value) {
        data.fill(value);
    }

    explicit mat(const std::array<std::array<T, N>, M> &values) {
        for (std::size_t i = 0; i < M; ++i) {
            for (std::size_t j = 0; j < N; ++j) {
                (*this)(i, j) = values[i][j];
            }
        }
    }

    //========== Operators ==========

    T &operator()(std::size_t i, std::size_t j) {
        if (i >= M || j >= N) throw std::out_of_range("Index out of range");
        return data[i * N + j];
    }

    const T &operator()(std::size_t i, std::size_t j) const {
        if (i >= M || j >= N) throw std::out_of_range("Index out of range");
        return data[i * N + j];
    }

    //========== Methods ==========

    [[nodiscard]] constexpr std::size_t m() const {
        return M;
    }

    [[nodiscard]] constexpr std::size_t n() const {
        return N;
    }

    std::array<T, M> col(std::size_t j) const {
        if (j >= N) throw std::out_of_range("Index out of range");
        std::array<T, M> column;
        for (std::size_t i = 0; i < M; ++i) {
            column[i] = (*this)(i, j);
        }
        return column;
    }

    std::array<T, N> row(std::size_t i) const {
        if (i >= M) throw std::out_of_range("Index out of range");
        std::array<T, N> row;
        for (std::size_t j = 0; j < N; ++j) {
            row[j] = (*this)(i, j);
        }
        return row;
    }
};

// Implementez dot(vec, vec) qui effectue un produit scalaire
// entre deux vecteurs

// ...Compléter ici...

// Implementez un operator* entre deux objets de type vec, qui effectue un
// produit dyadique (https://fr.wikipedia.org/wiki/Produit_dyadique)
// Genere une matrice m dans laquelle chaque valeur aux coordonnees (i,j)
// vaut u[i] * v[j].

// ...Compléter ici...

// Implementez un operator* qui multiplie les valeurs de u par n
// (en faisant une copie ou transfert du vector)

// ...Compléter ici...

// Implementez un produit matrice/vecteur via l'operator*

// ...Compléter ici...

// Implementez un produit vecteur/matrice via l'operator*

// ...Compléter ici...

// Implementez un produit matrice/matrice via l'operator*

// ...Compléter ici...
