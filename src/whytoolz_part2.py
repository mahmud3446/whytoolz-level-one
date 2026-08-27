"""
WhyToolz Part II: Sequence Manipulation

Great work getting through Part One!

In this section, you'll implement functions that work with sequences
and iterables in various ways: slicing, dropping elements, combining
sequences, extracting data, and more.

These functions return CONCRETE LISTS OR VALUES, not generators.
This makes them easier to understand and debug while you learn the algorithms.

Focus on:
- Slicing and subsetting sequences
- Working with iterables (anything you can loop over)
- Combining and transforming sequences
- Building reusable sequence operations
- Extracting data from collections

See: https://toolz.readthedocs.io/en/latest/api.html#itertoolz
"""


from collections import deque
from unittest import result


def islice(seq, *args):
    """
    Slice a sequence and return a list of elements.

    Similar to itertools.islice, this function allows you to extract
    a subset of elements from a sequence.

    This is the foundation function for many of the sequence manipulation
    functions in Part II.

    Args:
        seq: Input sequence (can be any iterable)
        *args: Either:
            - Single argument (stop): islice(seq, 5) returns first 5 elements
            - Two arguments (start, stop): islice(seq, 2, 5) returns elements at indices 2, 3, 4
            - Three arguments (start, stop, step): islice(seq, 0, 10, 2) returns every 2nd element

    Returns:
        List of sliced elements from seq

    Example:
        >>> islice([1, 2, 3, 4, 5], 3)
        [1, 2, 3]
        >>> islice([1, 2, 3, 4, 5], 1, 4)
        [2, 3, 4]
        >>> islice([1, 2, 3, 4, 5], 0, 5, 2)
        [1, 3, 5]

    Hint: Parse the *args to determine start, stop, and step values,
          then iterate through the sequence collecting appropriate elements into a list.
    """
    if len(args) == 1:
        start , stop, step = 0, args[0], 1
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1
    elif len(args) == 3:
        start, stop, step = args[0], args[1], args[2]
    else:
        raise ValueError("islice() takes 2 to 4 arguments (seq, start, stop[, step])")

    result = []
    for index, item in enumerate(seq):
        if index >= start and index < stop and (index - start) % step == 0:
            result.append(item)
        if index >= stop:
            break
    return result


def drop(n, seq):
    """
    Skip the first n elements and return the rest as a list.

    Discards the first n elements and returns everything after.

    Args:
        n: Number of elements to skip
        seq: Input sequence

    Returns:
        List of all elements after the first n

    Example:
        >>> drop(2, [1, 2, 3, 4, 5])
        [3, 4, 5]
        >>> drop(3, 'hello')
        ['l', 'o']

    Hint: Use islice with a start parameter
    """
    from itertools import islice

    return list(islice(seq, n, None))



def tail(n, seq):
    """
    Return the last n elements from a sequence.

    Note: Unlike take/drop, this returns a list (not a generator)
    because we need to see the whole sequence to know what the
    last n elements are.

    Args:
        n: Number of elements from the end
        seq: Input sequence

    Returns:
        List of the last n elements

    Example:
        >>> tail(2, [1, 2, 3, 4, 5])
        [4, 5]
        >>> tail(3, 'hello')
        ['l', 'l', 'o']

    Hint: Use collections.deque with maxlen, or convert to list and slice
    """
    from collections import deque

    if n <= 0:
        return []
    return list(deque(seq, maxlen=n))

def concat(seqs):
    """
    Concatenate multiple sequences into a single list.

    Takes an iterable of iterables and returns all elements
    from all sequences in order.

    Args:
        seqs: An iterable of iterables

    Returns:
        List of all elements from all sequences

    Example:
        >>> concat([[1, 2], [3, 4], [5]])
        [1, 2, 3, 4, 5]
        >>> concat(['ab', 'cd', 'ef'])
        ['a', 'b', 'c', 'd', 'e', 'f']

    Hint: Nested loops to collect elements, or flatten the sequences
    """
    result = []
    for seq in seqs:
        for item in seq:
            result.append(item)
    return result


def unique(seq):
    """
    Return unique elements from a sequence, preserving order.

    Only returns each distinct element once, in the order of first appearance.

    Args:
        seq: Input sequence (possibly with duplicates)

    Returns:
        List of unique elements in order of first appearance

    Example:
        >>> unique([1, 2, 3, 2, 1, 4])
        [1, 2, 3, 4]
        >>> unique('hello')
        ['h', 'e', 'l', 'o']

    Hint: Keep a set of seen elements, only collect if not seen before
    """

    seen = set()
    result = []

    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result



def partition(n, seq):
    """
    Partition a sequence into tuples of length n.

    Splits the sequence into non-overlapping chunks of size n.
    If the sequence length isn't divisible by n, the last partition
    will be shorter.

    Args:
        n: Size of each partition
        seq: Input sequence

    Returns:
        List of tuples, each of size n (last may be shorter)

    Example:
        >>> partition(2, [1, 2, 3, 4, 5])
        [(1, 2), (3, 4), (5,)]
        >>> partition(3, 'hello')
        [('h', 'e', 'l'), ('l', 'o')]

    Hint: Use islice in a loop to grab n items at a time
    """
    if n <= 0:
        raise ValueError("Partition size must be greater than 0")

    return [tuple(seq[i:i + n]) for i in range(0, len(seq), n)]


def interleave(seqs):
    """
    Interleave multiple sequences element by element.

    Takes elements alternately from each sequence until all are exhausted.
    Shorter sequences are skipped once exhausted.

    Args:
        seqs: Multiple sequences to interleave

    Returns:
        List of interleaved elements

    Example:
        >>> interleave([[1, 2], [3, 4], [5, 6]])
        [1, 3, 5, 2, 4, 6]
        >>> interleave(['ab', 'cd'])
        ['a', 'c', 'b', 'd']

    Hint: Use zip_longest to handle sequences of different lengths
    """
    from itertools import zip_longest

    result = []
    for group in zip_longest(*seqs, fillvalue=None):
        for item in group:
            if item is not None:
                result.append(item)
    return result


def pluck(key, seq):
    """
    Extract a specific key from a sequence of dictionaries.

    Returns the value of 'key' from each dictionary in seq.
    Useful for extracting a column from a list of records.

    Args:
        key: The key to extract from each dict
        seq: Sequence of dictionaries

    Returns:
        List of values corresponding to key from each dict

    Example:
        >>> people = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        >>> pluck('name', people)
        ['Alice', 'Bob']
        >>> pluck('age', people)
        [30, 25]

    Hint: Use a list comprehension to extract values
    """
    return [d[key] for d in seq]



def accumulate(func, seq, initial=None):
    """
    Return accumulated results of applying func to sequence elements.

    Like reduce(), but returns intermediate results at each step.
    This creates a list of running totals/accumulations.

    Args:
        func: Binary function to apply (takes two args, returns one)
        seq: Input sequence
        initial: Optional starting value

    Returns:
        List of accumulated values at each step

    Example:
        >>> accumulate(lambda x, y: x + y, [1, 2, 3, 4], 0)
        [0, 1, 3, 6, 10]
        >>> accumulate(lambda x, y: x * y, [1, 2, 3, 4], 1)
        [1, 1, 2, 6, 24]

    Hint: Keep a running accumulator, collect results at each step
    """
    result = []
    it = iter(seq)
    if initial is not None:
        acc = initial
        result.append(acc)
    else:
        try:
            acc = next(it)
            result.append(acc)
        except StopIteration:
            return result  # Empty sequence and no initial value

    for item in it:
        acc = func(acc, item)
        result.append(acc)

    return result


def sliding_window(n, seq):
    """
    Create a sliding window of size n over a sequence.

    Returns overlapping tuples of n consecutive elements.
    Each window slides one position from the previous.

    Args:
        n: Window size
        seq: Input sequence

    Returns:
        List of tuples, each containing n consecutive elements

    Example:
        >>> sliding_window(2, [1, 2, 3, 4])
        [(1, 2), (2, 3), (3, 4)]
        >>> sliding_window(3, 'hello')
        [('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o')]

    Hint: Use collections.deque with maxlen to maintain the window
    """

    window = deque(maxlen=n)
    result = []
    for item in seq:
        window.append(item)
        if len(window) == n:
            result.append(tuple(window))
    return result


def take_nth(n, seq):
    """
    Return every nth element from a sequence.

    Takes elements at positions 0, n, 2n, 3n, ...

    Args:
        n: Take every nth element
        seq: Input sequence

    Returns:
        List of every nth element

    Example:
        >>> take_nth(2, [0, 1, 2, 3, 4, 5, 6])
        [0, 2, 4, 6]
        >>> take_nth(3, 'hello world')
        ['h', 'l', 'o', 'l']

    Hint: Use enumerate to track position, collect when position % n == 0
    """
    return [item for i, item in enumerate(seq) if i % n == 0]
