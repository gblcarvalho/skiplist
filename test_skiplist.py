import unittest
from skiplist import Node, SkipList


class NodeTestCase(unittest.TestCase):
    def test_new_node(self):
        node = Node(1)
        self.assertIsInstance(node, Node)

    def test_node_item(self):
        item = 1
        node = Node(item)
        self.assertIs(item, node.item)

    def test_level_greater_or_equal_zero(self):
        node = Node(1)
        self.assertGreaterEqual(node.level, 0)

    def test_valid_level_generate(self):
        node = Node(1)
        self.assertGreaterEqual(node._generate_level(), 0)

    def test_next_list_len_is_equal_to_level_plus_one(self):
        node = Node(1)
        self.assertEqual(node.level + 1, len(node.next))

    def test_magic_methods(self):
        node = Node(5)
        node2 = Node(6)
        node3 = Node(3)

        self.assertLess(node, 6)
        self.assertLess(node, node2)
        with self.assertRaises(ValueError):
            node < 'node'

        self.assertLessEqual(node, 5)
        self.assertLessEqual(node, node)
        with self.assertRaises(ValueError):
            node <= 'node'

        self.assertGreater(node, 3)
        self.assertGreater(node, node3)
        with self.assertRaises(ValueError):
            node > 'node'

        self.assertGreaterEqual(node, 5)
        self.assertGreaterEqual(node, node)
        with self.assertRaises(ValueError):
            node >= 'node'

        self.assertEqual(node, 5)
        self.assertEqual(node, node)
        with self.assertRaises(ValueError):
            node == 'node'

        self.assertNotEqual(node, 6)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, None)
        with self.assertRaises(ValueError):
            node != 'node'

    def test_getitem_next(self):
        node = Node(1)
        self.assertEqual(node[0], node.next[0])

    def test_setitem_next(self):
        node = Node(1)
        node2 = Node(2)
        node[0] = node2
        self.assertEqual(node.next[0], node2)

    def test_len_is_equal_to_next_len(self):
        node = Node(1)
        self.assertEqual(len(node), len(node.next))

    def test_dunder_repr(self):
        item = 1
        node = Node(item)
        self.assertEqual(str(node), str(item))


class SkipListTestCase(unittest.TestCase):
    def test_new_skiplist(self):
        skiplist = SkipList()
        self.assertIsInstance(skiplist, SkipList)

    def test_skiplist_head(self):
        skiplist = SkipList()
        self.assertIsInstance(skiplist.head, Node)

    def test_realloc_head_level_with_new_level(self):
        skiplist = SkipList()
        new_level = 10
        skiplist._realloc_head_level(new_level)
        self.assertEqual(new_level, skiplist.head.level)

    def test_realloc_head_level_with_decrement_is_greater_or_equal_zero(self):
        skiplist = SkipList()
        skiplist._realloc_head_level()
        self.assertGreaterEqual(skiplist.head.level, 0)

    def test_remove_none_head_next(self):
        skiplist = SkipList()
        skiplist._realloc_head_level(5)
        skiplist._realloc_head_level()
        if len(skiplist.head) > 1:
            self.assertNotEqual(skiplist.head[-2:], [None, None])
        else:
            self.assertEqual(skiplist.head[0], None)

    def test_head_next_list_len_is_equal_to_level_plus_one_after_increment_or_decrement_realloc(self):
        skiplist = SkipList()
        skiplist._realloc_head_level(10)
        self.assertEqual(skiplist.head.level + 1, len(skiplist.head))

        skiplist._realloc_head_level()
        self.assertEqual(skiplist.head.level + 1, len(skiplist.head))

    def test_insert_new_node(self):
        skiplist = SkipList()
        item = 1
        skiplist.insert(item)
        self.assertEqual(skiplist.head[0].item, item)

    def test_head_should_has_the_biggest_level(self):
        skiplist = SkipList()
        skiplist.insert(1)

        curr_node = skiplist.head[0]
        while curr_node:
            self.assertLessEqual(curr_node.level, skiplist.head.level)
            curr_node = curr_node[0]

    def test_skiplist_is_right_on_level_zero(self):
        skiplist = SkipList()

        items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for item in items:
            skiplist.insert(item)

        curr_node = skiplist.head[0]
        curr_item = 0

        while curr_node:
            self.assertEqual(curr_node, items[curr_item])
            curr_node = curr_node[0]
            curr_item += 1

    def test_head_next_update_on_insert(self):
        skiplist = SkipList()
        item = 1
        skiplist.insert(item)

        first_node = skiplist.head[0]
        level_aux = skiplist.head.level
        while level_aux >= 0:
            if level_aux <= first_node.level:
                self.assertEqual(skiplist.head[level_aux], first_node)
            else:
                self.assertEqual(skiplist.head[level_aux], None)
            level_aux -= 1

    def test_node_next_update_on_insert(self):
        skiplist = SkipList()
        for item in [1, 2, 3, 4]:
            skiplist.insert(item)

        level_nodes = {}
        curr_node = skiplist.head
        while curr_node:
            level_nodes[curr_node.item] = curr_node.level
            curr_node = curr_node[0]

        nodes_in_level = { level: [] for level in range(0, skiplist.head.level + 1)}

        level_aux = skiplist.head.level
        while level_aux >= 0:
            curr_node = skiplist.head
            while curr_node:
                nodes_in_level[level_aux].append(curr_node.item)
                curr_node = curr_node[level_aux]
            level_aux -= 1

        for item, level in level_nodes.items():
            self.assertIn(item, nodes_in_level[level])

    def test_search_item(self):
        skiplist = SkipList()
        item = 1
        skiplist.insert(item)
        self.assertEqual(skiplist.search(item), item)

    def test_return_none_if_item_not_in_skiplist_on_search(self):
        skiplist = SkipList()
        items = [1, 2, 3, 4]
        for item in items:
            skiplist.insert(item)

        self.assertIs(skiplist.search(10), None)

    def test_cant_insert_repeated_item(self):
        skiplist = SkipList()
        skiplist.insert(1)

        with self.assertRaises(ValueError):
            skiplist.insert(1)

    def test_remove_item(self):
        skiplist = SkipList()

        items = [1, 2, 3, 4, 5]
        for item in items:
            skiplist.insert(item)

        item = skiplist.remove(2)
        self.assertEqual(item, 2)
        self.assertIs(skiplist.search(2), None)

    def test_head_next_update_on_remove(self):
        skiplist = SkipList()

        items = [1, 2]
        for item in items:
            skiplist.insert(item)

        second_node = skiplist.head[0][0]

        skiplist.remove(1)

        level_aux = skiplist.head.level

        while level_aux >= 0:
            if level_aux <= second_node.level:
                self.assertEqual(skiplist.head[level_aux], second_node)
            else:
                self.assertEqual(skiplist.head[level_aux], None)
            level_aux -= 1

    def test_node_next_update_on_remove(self):
        skiplist = SkipList()
        for item in [1, 2, 3, 4, 5, 6]:
            skiplist.insert(item)

        skiplist.remove(3)
        skiplist.remove(5)

        level_nodes = {}
        curr_node = skiplist.head
        while curr_node:
            level_nodes[curr_node.item] = curr_node.level
            curr_node = curr_node[0]

        nodes_in_level = { level: [] for level in range(0, skiplist.head.level + 1)}

        level_aux = skiplist.head.level
        while level_aux >= 0:
            curr_node = skiplist.head
            while curr_node:
                nodes_in_level[level_aux].append(curr_node.item)
                curr_node = curr_node[level_aux]
            level_aux -= 1

        for item, level in level_nodes.items():
            self.assertIn(item, nodes_in_level[level])


if __name__ == '__main__':
    unittest.main()