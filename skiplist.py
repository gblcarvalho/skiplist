import random


class Node(object):
    def __init__(self, item):
        self.item = item
        self.level = self._generate_level()
        self.next = [None for _ in range(0, self.level + 1)]

    def _generate_level(self):
        i = 0
        while random.choice((True, False, True)):
            i += 1
        return i

    def __le__(self, other):
        if isinstance(other, int):
            return self.item <= other
        elif isinstance(other, Node):
            return self.item <= other.item
        else:
            raise ValueError

    def __lt__(self, other):
        if isinstance(other, int):
            return self.item < other
        elif isinstance(other, Node):
            return self.item < other.item
        else:
            raise ValueError

    def __ge__(self, other):
        if isinstance(other, int):
            return self.item >= other
        elif isinstance(other, Node):
            return self.item >= other.item
        else:
            raise ValueError

    def __gt__(self, other):
        if isinstance(other, int):
            return self.item > other
        elif isinstance(other, Node):
            return self.item > other.item
        else:
            raise ValueError

    def __eq__(self, other):
        if isinstance(other, int):
            return self.item == other
        elif isinstance(other, Node):
            return self.item == other.item
        elif other is None:
            return False
        else:
            raise ValueError

    def __ne__(self, other):
        if isinstance(other, int):
            return self.item != other
        elif isinstance(other, Node):
            return self.item != other.item
        elif other is None:
            return True
        else:
            raise ValueError

    def __getitem__(self, item):
        return self.next[item]

    def __setitem__(self, key, value):
        self.next[key] = value

    def __len__(self):
        return len(self.next)

    def __repr__(self):
        return str(self.item)


class SkipList(object):
    def __init__(self):
        self.head = Node(0)

    def insert(self, item):

        if self.search(item):
            raise ValueError

        new_node = Node(item)

        if self.head.level < new_node.level:
            self._realloc_head_level(new_node.level)

        level_aux = new_node.level
        curr_node = self.head
        while level_aux >= 0:
            if curr_node[level_aux] is None or curr_node[level_aux] > new_node:
                new_node[level_aux], curr_node[level_aux] = curr_node[level_aux], new_node
                level_aux -= 1
            else:
                curr_node = curr_node[level_aux]

    def search(self, item):

        curr_node = self.head
        curr_level = self.head.level

        while curr_level >= 0:
            if curr_node[curr_level]:
                if curr_node[curr_level] == item:
                    return curr_node[curr_level].item
                elif curr_node[curr_level] < item:
                    curr_node = curr_node[curr_level]
                else:
                    curr_level -= 1
            else:
                curr_level -= 1
        return None

    def remove(self, item):

        curr_node = self.head
        curr_level = self.head.level
        node_removed = None

        while curr_level >= 0:
            if curr_node[curr_level]:
                if curr_node[curr_level] == item:
                    if not node_removed:
                        node_removed = curr_node[curr_level]

                    curr_node[curr_level] = curr_node[curr_level][curr_level]
                    curr_level -= 1
                elif curr_node[curr_level] < item:
                    curr_node = curr_node[curr_level]
                else:
                    curr_level -= 1
            else:
                curr_level -= 1

        self._realloc_head_level()

        return node_removed

    def _realloc_head_level(self, new_level=None):
        if new_level:
            self.head.next.extend([None for _ in range(self.head.level, new_level)])
            self.head.level = new_level
        else:
            while len(self.head) > 1:
                if not self.head[-1]:
                    self.head.next.pop()
                    self.head.level -= 1
                else:
                    break
