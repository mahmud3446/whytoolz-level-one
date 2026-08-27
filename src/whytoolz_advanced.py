"""
WhyToolz Part IV: Advanced - Optional Challenge Functions

These functions are more complex and are meant for students who
finish early or want extra challenges.

These teach:
- Generators and lazy evaluation (infinite sequences)
- Advanced algorithms (heaps, SQL-like operations)
- Complex function composition
- Partial application

Good luck!
"""


def take(n, seq):
    """
    Return the first n elements from a sequence as a generator.

    This is a lazy version that yields elements one at a time.
    Unlike the list-based version, this doesn't consume the entire sequence upfront.

    Args:
        n: Number of elements to take
        seq: Input sequence

    Returns:
        Generator yielding the first n elements from seq

    Example:
        >>> list(take(3, [1, 2, 3, 4, 5]))
        [1, 2, 3]
        >>> list(take(2, 'hello'))
        ['h', 'e']

    Hint: Use 'yield' and enumerate or a counter to track how many items yielded
    """
    if n <= 0:
        return

    for index, item in enumerate(seq):
        yield item
        if index + 1 >= n:
            break


def iterate(func, x):
    """
    Create an infinite iterator by repeatedly applying func to x.

    Yields: x, func(x), func(func(x)), func(func(func(x))), ...

    This is a generator function that creates INFINITE sequences.
    You'll need to use take() or similar to limit the results.

    Args:
        func: Function to repeatedly apply
        x: Initial value

    Returns:
        Generator yielding infinite sequence of applications

    Example:
        >>> list(take(5, iterate(lambda x: x * 2, 1)))
        [1, 2, 4, 8, 16]
        >>> list(take(4, iterate(lambda x: x + 1, 0)))
        [0, 1, 2, 3]

    Hint: Use 'yield' to create a generator. Loop forever!
    """
    while True:
        yield x
        x = func(x)


def topk(k, seq):
    """
    Return the k largest elements from a sequence.

    Returns the top k elements in descending order.
    Uses a heap for efficiency.

    Args:
        k: Number of elements to return
        seq: Input sequence

    Returns:
        List of k largest elements (descending order)

    Example:
        >>> topk(3, [1, 5, 3, 9, 2, 7])
        [9, 7, 5]
        >>> topk(2, 'hello world')
        ['w', 'r']

    Hint: Use heapq.nlargest
    """
    import heapq
    return heapq.nlargest(k, seq)


def reduceby(key, binop, seq, init):
    """
    Simultaneously group and reduce a sequence.

    Like groupby() followed by reduce() on each group, but more efficient.
    Groups items by key function, then reduces each group using binop.

    Args:
        key: Function to compute grouping key
        binop: Binary reduction function
        seq: Input sequence
        init: Initial value for each reduction

    Returns:
        Dictionary mapping keys to reduced values

    Example:
        >>> data = [('a', 1), ('b', 2), ('a', 3), ('b', 4)]
        >>> reduceby(lambda x: x[0], lambda acc, x: acc + x[1], data, 0)
        {'a': 4, 'b': 6}

    Hint: Build a dict while iterating, reducing as you go
    """
    result = {}
    for item in seq:
        k = key(item)
        if k not in result:
            result[k] = init
        result[k] = binop(result[k], item)
    return result


def juxt(*funcs):
    """
    Create a function that applies multiple functions to the same argument.

    Returns a function that, when called with x, returns a tuple of
    (func1(x), func2(x), func3(x), ...)

    Args:
        *funcs: Functions to apply

    Returns:
        Function that returns tuple of results

    Example:
        >>> f = juxt(lambda x: x * 2, lambda x: x + 1, lambda x: x ** 2)
        >>> f(3)
        (6, 4, 9)

    Hint: Return a function that calls each func and returns tuple of results
    """
    def inner(x):
        return tuple(func(x) for func in funcs)
    return inner


def curry(func):
    """
    Transform a function to support partial application.

    Returns a curried version of func that can be called with fewer
    arguments than required, returning a new function that takes the
    remaining arguments.

    Args:
        func: Function to curry

    Returns:
        Curried version of func

    Example:
        >>> def add(a, b, c):
        ...     return a + b + c
        >>> curried_add = curry(add)
        >>> curried_add(1)(2)(3)
        6
        >>> add_5 = curried_add(5)
        >>> add_5(10, 20)
        35

    Warning: This is VERY HARD! Requires inspect module and closures.
    Hint: Use functools.partial or inspect.signature
    """
    from functools import partial
    from inspect import signature

    def curried(*args):
        if len(args) >= len(signature(func).parameters):
            return func(*args)
        return partial(curried, *args)

    return curried