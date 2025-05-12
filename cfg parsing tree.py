class CFG:
    def __init__(self):
        self.rules = {}  

    def add_rule(self, lhs, rhs_list):
        if lhs not in self.rules:
            self.rules[lhs] = []
        for rhs in rhs_list:
            self.rules[lhs].append(rhs)

    def parse(self, start_symbol, input_string):
       
        parses = self._parse_recursive(start_symbol, input_string, 0)
        return len([p for p in parses if p[1] == len(input_string)]) > 1

    def _parse_recursive(self, symbol, input_string, pos):
        results = []

        
        if symbol.islower():
            if pos < len(input_string) and input_string[pos] == symbol:
                results.append(([symbol], pos + 1))
            return results

        if symbol not in self.rules:
            return []

        for production in self.rules[symbol]:
            current_pos = pos
            current_tree = [symbol]
            sub_trees = []
            valid = True

            for sym in production:
                sub_results = self._parse_recursive(sym, input_string, current_pos)
                if not sub_results:
                    valid = False
                    break
                
                new_subtrees = []
                for subtree, next_pos in sub_results:
                    for existing in sub_trees or [[]]:
                        new_subtrees.append(existing + [subtree])
                sub_trees = new_subtrees
                current_pos = sub_results[0][1]  

            if valid:
                for t in sub_trees:
                    results.append(([symbol] + t, current_pos))

        return results


def main():
    grammar = CFG()
    # Example CFG: S -> AB | BA, A -> a, B -> b
    grammar.add_rule("S", [["A", "B"], ["B", "A"]])
    grammar.add_rule("A", [["a"]])
    grammar.add_rule("B", [["b"]])

    input_string = "ab"

    is_ambiguous = grammar.parse("S", input_string)
    if is_ambiguous:
        print(f"The grammar is ambiguous for the string '{input_string}'.")
    else:
        print(f"The grammar is unambiguous for the string '{input_string}'.")

if __name__ == "__main__":
    main()
