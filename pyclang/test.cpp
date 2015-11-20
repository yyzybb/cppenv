#include "test.h"

template <class H, int V>
struct A {

    template <class T, typename U = int, int X = 2>
    float* foo(T arg, double & db);

    struct In;
    In bar(In& a);

    static void fb() {}
};

void foo(A* a);
