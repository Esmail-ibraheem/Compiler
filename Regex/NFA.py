class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def is_accepting(self, state):
        return state in self.accepting_states

    def transition(self, state, symbol):
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        else:
            return set()

    def is_accepted(self, input_string):
        current_states = set([self.initial_state])

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states |= self.transition(state, symbol)
            current_states = next_states

        return any(self.is_accepting(state) for state in current_states)
    
    def print_rules(self):
        print("accept more than one state at once")
        print("accept the ε moves")
        print("accept more than one transition")


class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def is_accepting(self, state):
        return state in self.accepting_states

    def transition(self, state, symbol):
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        else:
            return None

    def is_accepted(self, input_string):
        current_state = self.initial_state

        for symbol in input_string:
            current_state = self.transition(current_state, symbol)
            if current_state is None:
                return False

        return self.is_accepting(current_state)

    def print_rules(self):
        print("accept single state")
        print("do not accept the ε moves")
        print("accept one transition") 

# Example usage:
if __name__ == "__main__":

    states = {'q0', 'q1', 'q2'}
    alphabet = {'0', '1'}
    transitions_1 = {
        'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
        'q1': {'1': {'q2'}}
    }
    initial_state = 'q0'
    accepting_states = {'q2'}

    nfa = NFA(states, alphabet, transitions_1, initial_state, accepting_states)

    # Test input strings
    test_strings = ['101', '1001', '000', '111', '10']
    for string in test_strings:
        if nfa.is_accepted(string):
            print(f'String "{string}" is accepted.')
        else:
            print(f'String "{string}" is not accepted.')
    print("Complexity: O(mn^2), lower memory higher scan time")
    nfa.print_rules()

    print("####################################################")
    # Define the DFA
    # states = {'q0', 'q1', 'q2'}
    alphabet = {'0', '1'}
    transitions_2 = {
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q2'}
    }
    initial_state = 'q0'
    accepting_states = {'q2'}

    dfa = DFA(states, alphabet, transitions_2, initial_state, accepting_states)

    # Test input strings
    test_strings = ['101', '1001', '000', '111', '10']
    for string in test_strings:
        if dfa.is_accepted(string):
            print(f'String "{string}" is accepted.')
        else:
            print(f'String "{string}" is not accepted.')
    print("Complexity: O(m), higher memory lower scan time")
    dfa.print_rules()

    print("##################################")