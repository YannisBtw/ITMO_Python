# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False
from cython.parallel cimport prange, threadid
from libc.math cimport sin
from libc.stdlib cimport calloc, free

cpdef double integrate_sin_nogil(double a, double b, long n_iter, int n_threads=2):
    """
    Итерация 5: интегрирование sin(x) без GIL с распараллеливанием по потокам.

    Важно:
    - общий total нельзя увеличивать из разных потоков (гонка данных)
    - поэтому используем массив частичных сумм (по одному на поток)
    - затем суммируем частичные суммы после выхода из nogil
    """
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef int nt = n_threads
    cdef double* partial = <double*> calloc(nt, sizeof(double))
    cdef int tid
    cdef double total = 0.0

    if partial == NULL:
        raise MemoryError()

    try:
        with nogil:
            for i in prange(n_iter, schedule='static', num_threads=nt):
                tid = threadid()
                partial[tid] += sin(a + i * step) * step

        # суммируем уже под GIL (здесь уже нет гонок)
        for i in range(nt):
            total += partial[i]
        return total
    finally:
        free(partial)
