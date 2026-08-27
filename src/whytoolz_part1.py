"""
WhyToolz Part I: Foundation - Working with Concrete Data Structures

In this section, you'll implement basic functions that work with lists,
dictionaries, and single values. These functions return concrete data
(not generators), making them easier to understand and debug.

Focus on:
- Understanding function signatures and return types
- Working with Python's indexing and slicing
- Building dictionaries from scratch
- Recursion for nested structures

See: https://toolz.readthedocs.io/en/latest/api.html#itertoolz
"""


def identity(x):
    """
    Return the input unchanged.

    While this seems trivial, identity is useful as a default function
    when no transformation is needed.

    Args:
        x: Any value

    Returns:
        The same value unchanged

    Example:
        >>> identity(5)
        5
        >>> identity([1, 2, 3])
        [1, 2, 3]
    """
    return x


def first(seq):
    """
    Return the first element of a sequence.

    Args:
        seq: Any iterable sequence

    Returns:
        The first element

    Example:
        >>> first([1, 2, 3])
        1
        >>> first("hello")
        'h'

    Hint: How do you safely get the first element of any iterable?
    """
    return next(iter(seq))


def second(seq):
    """
    Return the second element of a sequence.

    Args:
        seq: Any iterable sequence

    Returns:
        The second element

    Example:
        >>> second([1, 2, 3])
        2
        >>> second("hello")
        'e'
    """
    return next(iter(seq[1:]))


def last(seq):
    """
    Return the last element of a sequence.

    Args:
        seq: Any iterable sequence

    Returns:
        The last element

    Example:
        >>> last([1, 2, 3])
        3
        >>> last("hello")
        'o'

    Hint: Can you do this without converting the entire iterable to a list?
    """
    return next(iter(seq[::-1]))


def nth(n, seq):
    """
    Return the nth element of a sequence (0-indexed).

    Args:
        n: Index of element to retrieve (0-based)
        seq: Any iterable sequence

    Returns:
        The element at position n

    Example:
        >>> nth(2, [1, 2, 3, 4, 5])
        3
        >>> nth(0, "hello")
        'h'

    Raises:
        IndexError: If n is out of bounds
    """
    return next(iter(seq[n:]))


def count(seq):
    """
    Count the number of items in an iterable.

    Note: This exhausts the iterable! Unlike len(), this works on
    any iterable including generators.

    Args:
        seq: Any iterable

    Returns:
        The number of items

    Example:
        >>> count([1, 2, 3])
        3
        >>> count(range(10))
        10

    Hint: You'll need to consume the entire iterable to count it.
    """
    return sum(1 for _ in seq)


def frequencies(seq):
    """
    Count the occurrences of each unique item in a sequence.

    Returns a dictionary mapping each unique item to its count.

    Args:
        seq: Any iterable

    Returns:
        Dictionary of {item: count}

    Example:
        >>> frequencies(['a', 'b', 'a', 'c', 'b', 'a'])
        {'a': 3, 'b': 2, 'c': 1}
        >>> frequencies([1, 1, 2, 3, 2, 1])
        {1: 3, 2: 2, 3: 1}

    Hint: Build a dictionary from scratch, updating counts as you iterate.
    """
    freq = {}
    for item in seq:
        freq[item] = freq.get(item, 0) + 1
    return freq


def groupby(key, seq):
    """
    Group items in a sequence by the result of a key function.

    Returns a dictionary where keys are the results of calling key(item)
    and values are lists of items that produced that key.

    Args:
        key: Function to compute grouping key for each item
        seq: Iterable to group

    Returns:
        Dictionary mapping keys to lists of items

    Example:
        >>> groupby(len, ['a', 'bb', 'ccc', 'dd', 'e'])
        {1: ['a', 'e'], 2: ['bb', 'dd'], 3: ['ccc']}
        >>> groupby(lambda x: x % 2, [1, 2, 3, 4, 5])
        {1: [1, 3, 5], 0: [2, 4]}

    Hint: Similar to frequencies, but storing lists of items instead of counts.
    """
    groups = {}
    for item in seq:
        key_val = key(item)
        if key_val not in groups:
            groups[key_val] = []
        groups[key_val].append(item)
    return groups


def cons(el, seq):
    """
    Prepend an element to the beginning of a sequence.

    Returns a new list with el as the first element, followed by
    all elements from seq. The original sequence is not modified.

    Args:
        el: Element to prepend
        seq: Sequence to prepend to

    Returns:
        New list with el at the front

    Example:
        >>> cons(1, [2, 3, 4])
        [1, 2, 3, 4]
        >>> cons('a', 'bcd')
        ['a', 'b', 'c', 'd']

    Hint: This should return a list, not a generator.
    """
    return [el] + list(seq)


def merge(*dicts):
    """
    Merge multiple dictionaries into one.

    Later dictionaries take precedence - if the same key appears
    in multiple dicts, the value from the rightmost dict wins.

    Args:
        *dicts: Variable number of dictionaries to merge

    Returns:
        New dictionary with all key-value pairs

    Example:
        >>> merge({'a': 1}, {'b': 2}, {'c': 3})
        {'a': 1, 'b': 2, 'c': 3}
        >>> merge({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
        {'a': 1, 'b': 3, 'c': 4}

    Hint: Iterate through dicts and update a result dictionary.
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result
