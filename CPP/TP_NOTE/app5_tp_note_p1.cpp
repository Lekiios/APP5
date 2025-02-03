/**
 * APP5 IIM
 * GUILLEMONT Vladimir
 * DUAULT Gaston
 * LACZKOWSKI Lorenzo
 */

#include <iostream>
#include <cmath>
#include <tuple>
#include <algorithm>

//--------------------------------------------------------------------------------------
/*
  Le but de ce TP est de mettre en place un petit système d'EXPRESSION TEMPLATES
  Les EXPRESSION TEMPLATES sont une technique d'optimisation de calcul numérique qui
  utilisent la méta-programmation pour construire une représentation légére d'une formule
  arbitraire sous la forme d'un ARBRE DE SYNTAXE ABSTRAITE.

  Une fois construit à la compilation, cet arbre devient exploitable à la compilation 
  ou à l'exécution pour effectuer des calculs de divers types. 

  Répondez au questions dans l'ordre en complétant le code.
*/
//---------------------------------------------------------------------------------------
namespace et {
    // Q1 - Définissez un concept expr qui est valide si un type T fournit un membre T::is_expr()
    template<typename T>
    concept expr = requires(T t)
    {
        { T::is_expr() };
    };

    //---------------------------------------------------------------------------------------
    /*
      Le premier élément fondamental d'un systeme d'EXPRESSION TEMPLATE est la classe de
      terminal. Un TERMINAL représente une feuille de l'ARBRE DE SYNTAXE. Dans notre cas,
      nos terminaux sont numéroté statiquement pour représent différentes variables.

      Q2. Complétez l'implémentation de la structure template terminal ci dessous en suivant les demandes
    */
    //---------------------------------------------------------------------------------------
    template<int ID>
    struct terminal {
        // Faite en sorte que terminal vérifie le concept expr
        static constexpr void is_expr() {
        }

        std::ostream &print(std::ostream &os) const {
            // Pour terminal<ID>, affiche "arg<ID>" et renvoit os.
            os << "arg<" << ID << ">";
            return os;
        }

        template<typename... Args>
        constexpr auto operator()(Args &&... args) const {
            // Construit un tuple de tout les args et renvoit le ID-eme via std::get
            // Veillez à bien repsecter le fait que args est une reference universelle
            auto tuple = std::forward_as_tuple(std::forward<Args>(args)...);
            return std::get<ID>(tuple);
        }
    };


    // Generateur de variable numérotée
    template<int ID>
    inline constexpr auto arg = terminal<ID>{};

    // Variables _0, _1 et _2 sont prédéfinies
    inline constexpr auto _0 = arg<0>;
    inline constexpr auto _1 = arg<1>;
    inline constexpr auto _2 = arg<2>;

    //---------------------------------------------------------------------------------------
    /*
      Le deuxieme élément  d'un systeme d'EXPRESSION TEMPLATE est la classe de noeud.
      Un NODE représente un opératuer ou une fonction dans l'ARBRE DE SYNTAXE.

      Il est définit par le type de l'OPERATION effectuée au passage du noeud et d'une
      liste variadique de ses sous-nodes.

      Q3 Complétez l'implémentation de la structure template node ci dessous en suivant les demandes
    */
    //---------------------------------------------------------------------------------------
    template<typename Op, typename... Children>
    struct node {
        // Faite en sorte que node vérifie le concept expr
        static constexpr void is_expr() {
        }

        // Construisez un node à partir d'une instande de Op et d'une liste variadique de Children
        // Ce constructeur sera constexpr
        // === use make_tuple to make a copy instead of reference with forward_as_tuple ===
        constexpr explicit node(Op _op, Children... _children) : op(std::move(_op)),
                                                                 children(_children...) {
        }

        // L'operateur() de node permet d'avaluer le sous arbre courant de manière
        // récursive. Les paramètres args... représentent dans l'ordre les valeurs des
        // variables contenus dans le sous arbre.
        // Par exemple, le node {op_add, terminal<1>, termnal<0>} appelant operator()(4, 9)
        // doit renvoyer op_add(9, 4);
        // Renseignez vous sur std::apply pour vous simplifier la vie
        // Pensez qu'un node contient potentiellement d'autre node.
        template<typename... Args>
        constexpr auto operator()(Args &&... args) const {
            return std::apply(
                [&](const auto &... child) { return op(child(std::forward<Args>(args)...)...); },
                children);
        }

        // Affiche un node en demandant à Op d'afficher les sous arbres
        std::ostream &print(std::ostream &os) const {
            std::apply(
                [&](const auto &... child) {
                    op.print(os, child...);
                },
                children
            );
            return os;
        }

        // Op est stockée par valeur
        // les Children... sont stockées dans un tuple
        Op op;

        std::tuple<Children...> children;
    };

    //----------------------------------------------
    /*
      add_ est un exemple de type d'operation passable à un node
      Il fournit un operator() qui effectue le calcul et une fonction
      print qui affiche le node.
    */
    //----------------------------------------------
    struct add_ {
        constexpr auto operator()(auto a, auto b) const {
            return a + b;
        }

        std::ostream &print(std::ostream &os, auto a, auto b) const {
            return os << a << " + " << b;
        }
    };

    // On lui associe un operator+ qui consomme des expr et renvoit le node
    template<expr L, expr R>
    constexpr auto operator+(L l, R r) {
        return node{add_{}, l, r};
    }

    /*
      Q4. Sur le modèle de add_, implémentez
        - mul_ et un operator* pour la multiplication
        - abs_ et une fonction abs pour le calcul de la valeur absolue
        - fma_ et une fonction fma(a,b,c) qui calcul a*b+c
    */

    // mul_
    struct mul_ {
        constexpr auto operator()(auto a, auto b) const {
            return a * b;
        }

        std::ostream &print(std::ostream &os, auto a, auto b) const {
            return os << a << " * " << b;
        }
    };

    // On lui associe un operator* qui consomme des expr et renvoit le node
    template<expr L, expr R>
    constexpr auto operator*(L l, R r) {
        return node{mul_{}, l, r};
    }

    // abs_
    struct abs_ {
        constexpr auto operator()(auto a) const {
            return std::abs(a);
        }

        std::ostream &print(std::ostream &os, auto a) const {
            return os << "|" << a << "|";
        }
    };

    // On lui associe une fonction abs qui consomme une expr et renvoit le node
    template<expr R>
    constexpr auto abs(R r) {
        return node{abs_{}, r};
    }

    // fma_
    struct fma_ {
        constexpr auto operator()(auto edward, auto alphonse, auto elric) const {
            return edward * alphonse + elric;
        }

        std::ostream &print(std::ostream &os, auto edward, auto alphonse, auto elric) const {
            //return os << "(" << edward << " * " << alphonse << " + " << elric << ")";
            return os << edward << " * " << alphonse << " + " << elric;
        }
    };

    // On lui associe une fonction fma qui consomme des expr et renvoit le node
    template<expr A, expr B, expr C>
    constexpr auto fma(A edward, B alphonse, C elric) {
        return node{fma_{}, edward, alphonse, elric};
    }


    std::ostream &operator<<(std::ostream &os, expr auto const &exprr) {
        return exprr.print(os);
    }
}


// Helpers to make tests
template<et::expr T>
constexpr void test_expr_concept() {
    std::cout << "J'ai vérifié que ce que tu m'as donné un type qui réponds au concept expr !" << std::endl;
}

int main() {
    // Q5. Le mini exemple ci dessous doit fonctionner. Complétez le avec une série de tests
    // exhaustif de tout les cas qui vous paraissent nécessaire.
    constexpr auto f = et::fma(et::_1, abs(et::_2), et::_0);

    f.print(std::cout) << std::endl;

    std::cout << f(1, 2, 3) << std::endl;


    // =============== TESTS ===============
    // Test concept expr
    struct test_expr {
        static constexpr bool is_expr() { return NULL; }
    };
    struct test_not_expr {
    };
    test_expr_concept<test_expr>();
    //test_expr_concept<test_not_expr>(); // Should not compile if uncommented

    // Test terminal
    std::cout << "======Tests terminal=======" << std::endl;
    constexpr auto t = et::terminal<0>{};
    t.print(std::cout) << std::endl;
    static_assert(t(1, 2, 3) == 1);

    constexpr auto t2 = et::terminal<5>{};
    t2.print(std::cout) << std::endl;
    static_assert(t2(12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1) == 7);

    // Test node
    std::cout << "=========Tests node========" << std::endl;
    constexpr auto n = t + t2;
    n.print(std::cout) << std::endl;

    // ============= Test expressions ===============
    std::cout << "=====Tests expressions=====" << std::endl;

    [[maybe_unused]] constexpr auto _t0 = et::terminal<0>{};
    [[maybe_unused]] constexpr auto _t1 = et::terminal<1>{};
    [[maybe_unused]] constexpr auto _t2 = et::terminal<2>{};
    [[maybe_unused]] constexpr auto _t3 = et::terminal<3>{};
    [[maybe_unused]] constexpr auto _t4 = et::terminal<4>{};
    [[maybe_unused]] constexpr auto _t5 = et::terminal<5>{};

    // test add_
    std::cout << "-------------------- add_ :" << std::endl;
    constexpr auto add1 = _t0 + _t1;
    add1.print(std::cout) << std::endl;
    static_assert(add1(1, 2) == 3);

    constexpr auto add2 = _t0 + _t1 + _t2;
    add2.print(std::cout) << std::endl;
    static_assert(add2(10, 20, 70) == 100);

    constexpr auto add3 = _t1 + _t5 + _t2 + _t0 + _t3 + _t4;
    add3.print(std::cout) << std::endl;
    static_assert(add3(1, 2, 3, 4, 5, 6) == 21);

    constexpr auto sum = add1 + add2 + add3;
    sum.print(std::cout) << std::endl;
    static_assert(sum(1, 2, 3, 4, 5, 6) == 30);

    // test mul_
    std::cout << "-------------------- mul_ :" << std::endl;
    constexpr auto mul1 = _t0 * _t1;
    mul1.print(std::cout) << std::endl;
    static_assert(mul1(1, 2) == 2);

    constexpr auto mul2 = _t0 * _t2 * _t3;
    mul2.print(std::cout) << std::endl;
    static_assert(mul2(1, 2, 4, 8) == 32);

    constexpr auto mul3 = mul1 * mul2;
    mul3.print(std::cout) << std::endl;
    static_assert(mul3(1, 2, 4, 8) == 64);

    // test abs_
    std::cout << "-------------------- abs_ :" << std::endl;
    constexpr auto abs1 = et::abs(_t0);
    abs1.print(std::cout) << std::endl;
    static_assert(abs1(-1, 2, 3) == 1);

    constexpr auto abs2 = et::abs(_t2);
    abs2.print(std::cout) << std::endl;
    static_assert(abs2(1, 2, 3) == 3);

    // test fma_
    std::cout << "-------------------- fma_ :" << std::endl;
    constexpr auto fma1 = et::fma(_t0, _t1, _t2);
    fma1.print(std::cout) << std::endl;
    static_assert(fma1(1, 2, 3) == 5);

    constexpr auto fma2 = et::fma(_t1, _t2, _t0);
    fma2.print(std::cout) << std::endl;
    static_assert(fma2(1, 2, 3) == 7);

    // Test full expressions
    std::cout << "-------- Full expressions :" << std::endl;
    constexpr auto full1 = et::fma(et::abs(_t0), _t1, et::fma(_t2, _t3, _t4));
    full1.print(std::cout) << std::endl;
    static_assert(full1(-2, 2, 3, 4, 5) == 21);

    constexpr auto full2 = et::fma(full1, add1, _t3) * et::abs(et::fma(_t5, _t0, _t2));
    full2.print(std::cout) << std::endl;
    static_assert(full2(-2, 2, 3, 4, 5, 2) == 4);
}
