def epsilon_closure(state, transitions):
    stack = [state] if isinstance(state, str) else list(state)
    closure = set(stack)
    
    while stack:
        current = stack.pop()
        for next_state in transitions.get(current, {}).get('ε', []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    
    return closure

def move(states, symbol, transitions):
    result = set()
    for state in states:
        result.update(transitions.get(state, {}).get(symbol, []))
    return result

def nfa_to_dfa(nfa):
    states = nfa['states']
    alphabet = nfa['alphabet']
    transitions = nfa['transitions']
    start_state = nfa['start_state']
    accept_states = nfa['accept_states']

    dfa_states = []
    dfa_start = frozenset(epsilon_closure(start_state, transitions))
    dfa_states_map = {dfa_start: 'A'}  
    unmarked_states = [dfa_start]
    dfa_transitions = {}
    dfa_accept_states = set()
    state_name_counter = ord('A') + 1  

    while unmarked_states:
        current = unmarked_states.pop()
        current_name = dfa_states_map[current]
        dfa_transitions[current_name] = {}

        for symbol in alphabet:
            move_result = move(current, symbol, transitions)
            closure = epsilon_closure(move_result, transitions)
            closure_frozen = frozenset(closure)

            if not closure:
                continue

            if closure_frozen not in dfa_states_map:
                dfa_states_map[closure_frozen] = chr(state_name_counter)
                state_name_counter += 1
                unmarked_states.append(closure_frozen)

            target_name = dfa_states_map[closure_frozen]
            dfa_transitions[current_name][symbol] = target_name

        if any(state in accept_states for state in current):
            dfa_accept_states.add(current_name)

    return {
        'states': set(dfa_transitions.keys()),
        'alphabet': alphabet,
        'transitions': dfa_transitions,
        'start_state': dfa_states_map[dfa_start],
        'accept_states': dfa_accept_states
    }
# Example NFA
nfa = {
    'states': {'q0', 'q1', 'q2'},
    'alphabet': {'0', '1'},
    'transitions': {
        'q0': {'ε': {'q1', 'q2'}},
        'q1': {'0': {'q1'}, '1': {'q1'}},
        'q2': {'1': {'q2'}}
    },
    'start_state': 'q0',
    'accept_states': {'q1'}
}

dfa = nfa_to_dfa(nfa)
for k, v in dfa.items():
    print(f"{k}: {v}")
