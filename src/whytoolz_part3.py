"""
WhyToolz Part III: Functions & Dictionaries - Composition and Transformation

Now that you understand both eager and lazy evaluation, let's explore
higher-order functions and dictionary operations.

Higher-order functions are functions that:
- Take other functions as arguments, OR
- Return functions as results

These are powerful tools for creating reusable, composable code.

Focus on:
- Function decorators (functions that return functions)
- Function composition (chaining functions together)
- Immutable dictionary operations
- Nested data structure traversal

See: https://toolz.readthedocs.io/en/latest/api.html#functoolz
See: https://toolz.readthedocs.io/en/latest/api.html#dicttoolz
"""


from functools import reduce


def pipe(data, *funcs):
    """
    Thread data through a sequence of functions (left to right).

    Applies each function to the result of the previous function,
    starting with data. This is similar to the | operator in shells.

    Args:
        data: Initial value
        *funcs: Functions to apply in order

    Returns:
        Result of applying all functions

    Example:
        >>> pipe(3, lambda x: x * 2, lambda x: x + 1)
        7
        >>> pipe([1, 2, 3], sum, lambda x: x * 2)
        12

    Hint: You could use a loop...
    """
    result = data
    for func in funcs:
        result = func(result)
    return result


def compose(*funcs):
    """
    Compose multiple functions into a single function (right to left).

    Returns a new function that applies funcs in reverse order.
    compose(f, g, h)(x) == f(g(h(x)))

    Args:
        *funcs: Functions to compose

    Returns:
        New function that applies all funcs right-to-left

    Example:
        >>> double = lambda x: x * 2
        >>> add_one = lambda x: x + 1
        >>> f = compose(add_one, double)
        >>> f(3)  # add_one(double(3)) = add_one(6) = 7
        7

    Hint: Return a function that calls each func in reverse order
    """

    def composed_function(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed_function


def complement(func):
    """
    Return a function that returns the opposite boolean of func.

    Creates a new function that negates the result of func.
    Useful for creating opposite predicates.

    Args:
        func: A predicate function (returns bool)

    Returns:
        New function that returns not func(...)

    Example:
        >>> is_even = lambda x: x % 2 == 0
        >>> is_odd = complement(is_even)
        >>> is_odd(3)
        True
        >>> is_odd(4)
        False

    Hint: Return a function that calls func and negates the result
    """
    def negated_function(*args, **kwargs):
        return not func(*args, **kwargs)
    return negated_function


def do(func, x):
    """
    Call func on x for side effects, then return x unchanged.

    Useful for inserting side effects (like logging) into a pipeline
    without changing the data flow.

    Args:
        func: Function to call for side effects
        x: Value to pass to func and return

    Returns:
        x (unchanged)

    Example:
        >>> def log(x):
        ...     print(f"Value: {x}")
        >>> pipe(5, lambda x: x * 2, lambda x: do(log, x), lambda x: x + 1)
        Value: 10
        11

    Hint: Call func(x), ignore result, return x
    """
    func(x)
    return x


def memoize(func):
    """
    Create a cached version of a function.

    Returns a new function that caches results based on arguments.
    If called with the same arguments again, returns cached result
    instead of recomputing.

    Args:
        func: Function to memoize

    Returns:
        Memoized version of func

    Example:
        >>> def expensive(x):
        ...     print(f"Computing {x}")
        ...     return x * 2
        >>> fast = memoize(expensive)
        >>> fast(5)
        Computing 5
        10
        >>> fast(5)  # Cached, no print
        10

    Hint: Use a dictionary to store {args: result} pairs
    """
    cache = {}
    def memoized_function(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memoized_function


def assoc(d, key, value):
    """
    Return a new dictionary with key set to value.

    Does NOT modify the original dictionary (immutable operation).

    Args:
        d: Original dictionary
        key: Key to set
        value: Value to associate with key

    Returns:
        New dictionary with key=value added/updated

    Example:
        >>> assoc({'a': 1}, 'b', 2)
        {'a': 1, 'b': 2}
        >>> assoc({'a': 1, 'b': 2}, 'b', 3)
        {'a': 1, 'b': 3}

    Hint: Create a copy of d and add the key-value pair
    """
    new_dict = d.copy()
    new_dict[key] = value
    return new_dict


def dissoc(d, *keys):
    """
    Return a new dictionary with specified keys removed.

    Does NOT modify the original dictionary (immutable operation).

    Args:
        d: Original dictionary
        *keys: Keys to remove

    Returns:
        New dictionary without specified keys

    Example:
        >>> dissoc({'a': 1, 'b': 2, 'c': 3}, 'b')
        {'a': 1, 'c': 3}
        >>> dissoc({'a': 1, 'b': 2, 'c': 3}, 'a', 'c')
        {'b': 2}

    Hint: Create a copy and remove keys, or use dict comprehension
    """
    return {k: v for k, v in d.items() if k not in keys}


def valmap(func, d):
    """
    Apply a function to all values in a dictionary.

    Returns a new dictionary with transformed values.
    Keys remain unchanged.

    Args:
        func: Function to apply to each value
        d: Original dictionary

    Returns:
        New dictionary with func applied to all values

    Example:
        >>> valmap(lambda x: x * 2, {'a': 1, 'b': 2})
        {'a': 2, 'b': 4}
        >>> valmap(str.upper, {'name': 'alice', 'city': 'boston'})
        {'name': 'ALICE', 'city': 'BOSTON'}

    Hint: Use dict comprehension
    """
    return {k: func(v) for k, v in d.items()}


def keymap(func, d):
    """
    Apply a function to all keys in a dictionary.

    Returns a new dictionary with transformed keys.
    Values remain unchanged.

    Args:
        func: Function to apply to each key
        d: Original dictionary

    Returns:
        New dictionary with func applied to all keys

    Example:
        >>> keymap(str.upper, {'a': 1, 'b': 2})
        {'A': 1, 'B': 2}
        >>> keymap(lambda x: x * 2, {1: 'a', 2: 'b'})
        {2: 'a', 4: 'b'}

    Hint: Use dict comprehension
    """
    return {func(k): v for k, v in d.items()}


def valfilter(predicate, d):
    """
    Filter dictionary by values that satisfy a predicate.

    Returns a new dictionary containing only key-value pairs
    where predicate(value) is True.

    Args:
        predicate: Function to test each value
        d: Original dictionary

    Returns:
        New dictionary with only passing values

    Example:
        >>> valfilter(lambda x: x > 2, {'a': 1, 'b': 3, 'c': 2, 'd': 4})
        {'b': 3, 'd': 4}
        >>> valfilter(lambda x: x % 2 == 0, {'a': 1, 'b': 2, 'c': 3})
        {'b': 2}

    Hint: Use dict comprehension with if clause
    """
    return {k: v for k, v in d.items() if predicate(v)}


def get_in(keys, d, default=None):
    """
    Get a value from a nested dictionary using a sequence of keys.

    Traverses nested dicts following the path specified by keys.
    Returns default if any key in the path doesn't exist.

    Args:
        keys: List of keys forming a path
        d: Nested dictionary
        default: Value to return if path doesn't exist

    Returns:
        Value at the end of the path, or default

    Example:
        >>> data = {'a': {'b': {'c': 1}}}
        >>> get_in(['a', 'b', 'c'], data)
        1
        >>> get_in(['a', 'x'], data, default='missing')
        'missing'

    Hint: Use a loop or recursion to traverse the path
    """
    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def update_in(d, keys, func):
    """
    Update a value in a nested dictionary using a function.

    Follows the path specified by keys, applies func to the value
    at that location, and returns a new nested dictionary with
    the updated value. The original dictionary is not modified.

    Args:
        d: Nested dictionary
        keys: List of keys forming a path
        func: Function to apply to value at path

    Returns:
        New nested dictionary with updated value

    Example:
        >>> data = {'a': {'b': {'c': 1}}}
        >>> update_in(data, ['a', 'b', 'c'], lambda x: x + 10)
        {'a': {'b': {'c': 11}}}

    Hint: This is tricky! You need to recursively copy and update nested dicts
    """
    if not keys:
        return func(d)
    key = keys[0]
    if isinstance(d, dict):
        new_d = d.copy()
        new_d[key] = update_in(d.get(key, {}), keys[1:], func)
        return new_d
    else:
        raise TypeError("Expected a dictionary at this level of nesting")