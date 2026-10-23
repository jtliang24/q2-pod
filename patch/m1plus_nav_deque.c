/* M1 Plus: deque_init_copy, which V2.1's demo doesn't export. patch/navigation.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
void deque_init_copy(void *dest, const void *src) {
    deque_init(dest);
    deque_assign(dest, src);
}

/* V2.1's demo imports no deque_pop_back (libcstl's is _deque_shrink_at_end(d, 1)): erase the last
 * element through the iterators it does import, so the deque keeps its own element type. */
void deque_pop_back(void *d) {
    if (!deque_size(d)) return;
    cstl_iter end = deque_end(d), last = deque_begin(d);
    for (cstl_iter it = iterator_next(last); !iterator_equal(it, end); it = iterator_next(it)) last = it;
    deque_erase(d, last);
}
#endif
