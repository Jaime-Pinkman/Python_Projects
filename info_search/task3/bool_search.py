class BooleanSearcher:
    @staticmethod
    def read_token_map(path) -> dict:
        token_map = {}
        with open(path, 'r', encoding="UTF-8") as file:
            for line in file:
                key = line.split(' ')[0]
                value = [int(i) for i in line[len(key) + 2:-2].replace(" ", "").split(',')]
                token_map[key] = value
        return token_map

    @staticmethod
    def update_token_set(token_map, token_set, token, operator, state):
        all_set = [i for i in range(100)]
        lst = token_map[token]
        if state is not None:
            lst = [i for i in all_set if i not in lst]
        if operator == 'and':
            token_set = [i for i in token_set if i in lst]
        elif operator == 'or':
            token_set = list(set([i for i in token_set] + [i for i in lst]))
        return token_set

    @staticmethod
    def run_query(query, token_map):
        tokens = query.split(' ')
        token_set = [i for i in range(100)]
        operator = 'and'

        while len(tokens) > 0:
            token = tokens.pop(0)
            if token == 'not':
                state = token
                token = tokens.pop(0)
                token_set = BooleanSearcher.update_token_set(token_map, token_set, token, operator, state)
            elif token == 'and' or token == 'or':
                operator = token
            else:
                state = None
                token_set = BooleanSearcher.update_token_set(token_map, token_set, token, operator, state)
        return token_set


if __name__ == "__main__":
    token_map = BooleanSearcher.read_token_map('token_map.txt')
    query = input()
    print(BooleanSearcher.run_query(query, token_map))
