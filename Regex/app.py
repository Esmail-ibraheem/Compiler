import streamlit as st
from NFA import NFA

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

# Streamlit app
def main():
    st.title("NFA to DFA Converter")

    # Input NFA details
    st.header("Enter NFA Details")
    nfa_states = st.text_input("NFA States (comma-separated)")
    nfa_alphabet = st.text_input("NFA Alphabet (comma-separated)")
    nfa_initial_state = st.text_input("NFA Initial State")
    nfa_accepting_states = st.text_input("NFA Accepting States (comma-separated)")

    nfa_states = set(nfa_states.split(','))
    nfa_alphabet = set(nfa_alphabet.split(','))
    nfa_accepting_states = set(nfa_accepting_states.split(','))

    nfa_transitions = {}
    for state in nfa_states:
        transitions = {}
        for symbol in nfa_alphabet:
            transition_str = st.text_input(f"Transition from state {state} with symbol {symbol} (comma-separated)")
            transitions[symbol] = set(transition_str.split(','))
        nfa_transitions[state] = transitions

    # Convert NFA to DFA
    if st.button("Convert NFA to DFA"):
        nfa = NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_initial_state, nfa_accepting_states)
        converter = NFAtoDFAConverter(nfa)
        dfa_info = converter.convert()

        # Display DFA details
        st.header("DFA Details")
        st.write("DFA States:", dfa_info['states'])
        st.write("DFA Transitions:", dfa_info['transitions'])
        st.write("DFA Initial State:", dfa_info['initial_state'])
        st.write("DFA Accepting States:", dfa_info['accepting_states'])

# Define NFA to DFA converter class
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

if __name__ == "__main__":
    main()
