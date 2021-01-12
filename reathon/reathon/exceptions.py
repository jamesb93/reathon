class InvalidNodeMethod(Exception):
    def __init__(self, node, method):
        super().__init__(f'{node} has no "{method}"')