from NFA-DFA import NFA

# State transition table
table = {
    'start': {
        'epsilon': ['start', '0'],
        'd': ['1'],
    },
    '0': {
        'epsilon': ['0', '4', '11'],
        'd': ['4'],
    },
    '1': {
        'd': ['2'],
    },
    '2': {
        'd': ['5'],
        'b': ['8'],
    },
    '4': {
        'epsilon': ['4', '11'],
        'u': ['6'],
    },
    '5': {
        'epsilon': ['5', '12'],
        'b': ['8'],
    },
    '6': {
        'u': ['3'],
        'b': ['8'],
    },
    '11': {
        'b': ['8'],
    },
    '12': {
        'epsilon': ['12'],
        'e': ['9'],
    },
    '3': {
        'u': ['3'],
        'e': ['10'],
    },
    '8': {
        'b': ['8'],
        'e': ['10'],
    },
    '9': {
        'e': ['9'],
    },
    '10': {
        'start': ['start'],
    }
}

# Function to follow the state transition table
def follow_table(table, state, input_string):
    for char in input_string:
        if char in table[state]:
            state = table[state][char][0]
        else:
            return False
    return state


class NFAtoDFAConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfa_states = set()
        self.dfa_transitions = {}
        self.dfa_initial_state = ''
        self.dfa_accepting_states = set()

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current_state = stack.pop()
            epsilon_transitions = self.nfa.transition(current_state, 'ε')
            for state in epsilon_transitions:
                if state not in closure:
                    closure.add(state)
                    stack.append(state)

        return closure

    def move(self, states, symbol):
        move_states = set()
        for state in states:
            move_states |= self.nfa.transition(state, symbol)
        return move_states

    def convert(self):
        self.dfa_states.clear()
        self.dfa_transitions.clear()
        self.dfa_accepting_states.clear()

        # Compute epsilon-closure of the initial state
        initial_epsilon_closure = self.epsilon_closure({self.nfa.initial_state})
        self.dfa_states.add(tuple(sorted(initial_epsilon_closure)))
        self.dfa_initial_state = tuple(sorted(initial_epsilon_closure))

        stack = [initial_epsilon_closure]

        while stack:
            current_states = stack.pop()
            current_states_tuple = tuple(sorted(current_states))

            # Check if the current states are accepting in the NFA
            for state in current_states:
                if self.nfa.is_accepting(state):
                    self.dfa_accepting_states.add(current_states_tuple)
                    break

            for symbol in self.nfa.alphabet:
                if symbol != 'ε':
                    move_states = self.move(current_states, symbol)
                    epsilon_closure_states = self.epsilon_closure(move_states)

                    if epsilon_closure_states:
                        epsilon_closure_tuple = tuple(sorted(epsilon_closure_states))
                        self.dfa_transitions.setdefault(current_states_tuple, {})[symbol] = epsilon_closure_tuple
                        if epsilon_closure_tuple not in self.dfa_states:
                            self.dfa_states.add(epsilon_closure_tuple)
                            stack.append(epsilon_closure_states)

        return {
            'states': self.dfa_states,
            'alphabet': self.nfa.alphabet,
            'transitions': self.dfa_transitions,
            'initial_state': self.dfa_initial_state,
            'accepting_states': self.dfa_accepting_states
        }


# Example usage:
if __name__ == "__main__":
    # Define the NFA
    print("another example")
    nfa_states = {'q0', 'q1', 'q2'}
    nfa_alphabet = {'0', '1', 'ε'}
    nfa_transitions = {
        'q0': {'0': {'q0', 'q1'}, '1': {'q0'}, 'ε': {'q1'}},
        'q1': {'1': {'q2'}},
        'q2': {'0': {'q2'}}
    }
    nfa_initial_state = 'q0'
    nfa_accepting_states = {'q2'}

    nfa = NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_initial_state, nfa_accepting_states)

    # Convert NFA to DFA
    converter = NFAtoDFAConverter(nfa)
    dfa_info = converter.convert()

    print("DFA States:", dfa_info['states'])
    print("DFA Transitions:", dfa_info['transitions'])
    print("DFA Initial State:", dfa_info['initial_state'])
    print("DFA Accepting States:", dfa_info['accepting_states'])

    print("####################################")
    print("The same example in the slides 264")
    # Example usage
    state = 'start'
    input_string = 'ddube'
    final_state = follow_table(table, state, input_string)
    if final_state == '10':
        print(f"The input string '{input_string}' is accepted by the DFA.")
    else:
        print(f"The input string '{input_string}' is not accepted by the DFA.")