#include "test.h"

struct xy;

template <class H, int V, class ... XArgs>
struct A {

    template <class T, typename U = int, int X = 2>
    float* foo(T arg, double & db);

    struct In;
    In* bar(In& a);

    In* fb(In& a, double b, void(*)(int)) const volatile &&;

    static void fb_defined() {}

    template <typename ... Args>
    int vars(Args && ... args);

    template <int ... Args>
    int bs();

//    void invalid_type(xy &);
};

class X;
void foo(X* a);

/*
template <typename  H, int  V, typename ... XArgs>
typename A<H, V, XArgs...>::In * A<H, V, XArgs...>::bar(A::In & a)
{

}
template <typename  H, int  V, typename ... XArgs>
typename A<H, V, XArgs...>::In * A<H, V, XArgs...>::fb(A::In & a, double b, void (*)(int) )volatile const && 
{

}
template <typename  H, int  V, typename ... XArgs>
template <typename ... Args>
int A<H, V, XArgs...>::vars(Args &&... args)
{

}
template <typename  H, int  V, typename ... XArgs>
template <int ... Args>
int A<H, V, XArgs...>::bs()
{

}

template <typename  H, int  V, typename ... XArgs>
template <typename  T, typename  U, int  X>
float * A<H, V, XArgs...>::foo(T arg, double & db)
{

}
*/
