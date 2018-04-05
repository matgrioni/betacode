# Based off of the original version by James Tauber. Cleaned up and refactored.

class Trie:
    """
    A simple trie class.
    """

    def __init__(self):
        """
        Create the Trie with an empty root.
        """
        self.root = [None, {}]

    def add(self, key, value):
        """
        Add an iterable key to the trie with an associated value.

        Args:
        key: The key to store in the Trie.
        value: The associated value to the key.
        """
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value

    def find(self, key):
        """
        Finds the given key in the Trie.

        Args:
        key: The key to search for in the trie.

        Returns:
        The associated value with the key if the key exists in the tree and None
        otherwise.
        """
        curr_node = self.root

        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None

        return curr_node[0]

    def find_prefix(self, key):
        """
        Finds a maximal prefix of the key in the trie if possible.

        Args:
        key: The key whose prefix will be searched for in the Trie.

        Returns:
        An ordered pair where the first value is the value found in the Trie
        from a prefix in the key and the second value is the remainder of the
        key.
        """
        curr_node = self.root
        remainder = key

        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]

        return (curr_node[0], remainder)
