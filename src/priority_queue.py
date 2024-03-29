def left(i):
    return (i * 2) + 1


def right(i):
    return (i * 2) + 2


def parent(i):
    return (i - 1) // 2


def min_heapify(q, i):
    l = left(i)
    r = right(i)
    min = i
    if l < len(q) and q[l] < q[min]:
        min = l
    if r < len(q) and q[r] < q[min]:
        min = r

    if min != i:
        q[min], q[i] = q[i], q[min]
        min_heapify(q, min)


def build(q):
    for i in range((len(q) // 2) + 1, 0, -1):
        min_heapify(q, i)


def enqueue(node, q):
    q.append(node)
    i = len(q) - 1
    while i >= 0 and q[parent(i)] > q[i]:
        q[parent(i)], q[i] = q[i], q[parent(i)]
        i = parent(i)


def deque(q):
    if len(q) == 0:
        raise Exception("No more items in queue")
    # swap elements
    q[0], q[len(q) - 1] = q[len(q) - 1], q[0]
    # decrement queue size
    min = q.pop()
    min_heapify(q, 0)
    if not is_valid(q):
        raise Exception("Produced incorrect min heap")
    return min


def is_valid(q):
    for i in range(len(q)):
        l = left(i)
        r = right(i)
        if l < len(q) and q[i] > q[l]:
            return False
        if r < len(q) and q[i] > q[r]:
            return False
    return True
