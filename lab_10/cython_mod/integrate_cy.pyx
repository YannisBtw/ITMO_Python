# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False
from libc.math cimport sin, cos

cdef inline double _poly2(double x) nogil:
    return x*x + 2.0*x + 1.0

cpdef double integrate_sin(double a, double b, long n_iter):
    # C-level loop, no Python calls in the loop.
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step
    return acc

cpdef double integrate_cos(double a, double b, long n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += cos(x) * step
    return acc

cpdef double integrate_poly2(double a, double b, long n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += _poly2(x) * step
    return acc

cpdef double integrate_pycall(object f, double a, double b, long n_iter):
    # Typed loop, but still calls Python function f(x) each iteration.
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += (<double>f(x)) * step
    return acc
