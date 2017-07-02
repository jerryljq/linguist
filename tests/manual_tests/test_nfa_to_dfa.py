from nfa_to_dfa import *
from tests.auto_tests.test_nfa_to_dfa import build_test_nfa
from pprint import pprint


def test_relabel_states():
    nfa = build_test_nfa()
    trans_matrix, starting_state, accepting_states = relabel_states(*subset_cons(nfa))
    pprint(trans_matrix)
    print(starting_state)
    print(accepting_states)


def test_nfa_to_dfa():
    nfa = build_test_nfa()
    dfa = nfa_to_dfa(nfa)
    pprint(dfa.trans_matrix)
    print(dfa.starting_state)
    print(dfa.accepting_states)
    print(dfa.alphabet)