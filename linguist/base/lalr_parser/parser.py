from linguist.base.lalr_parser.rule_set import Action
from linguist.base.lalr_parser.parser_base import d, t, nt
from linguist.base.metachar import epsilon
from linguist.exceptions import ParseError


def pop_len(derives):
    i = 0
    for x in derives:
        if x != t(epsilon):
            i += 1
    return i


class LALRParser:
    def __init__(self, rule_set, rule_actions):
        self.rule_set = rule_set
        self.cc, self.action, self.goto = self.rule_set.calc_parse_table()
        self.rule_actions = rule_actions

    def parse(self, tokens, repo=None):
        tokens = iter(tokens)
        data_stack = [None]
        state_stack = [0]
        token = next(tokens)
        while True:
            state = state_stack[-1]
            if token[0] not in self.action[state]:
                raise ParseError(self.action[state].keys(), token[0])
            else:
                action = self.action[state][token[0]]
                if action[0] == Action.accept:
                    ntid, rule_id = action[1:]
                    derives = self.rule_set.nt_rules[ntid][rule_id]
                    split_point = -len(derives)
                    data_list = data_stack[split_point:]
                    if self.rule_actions[(ntid, rule_id)] is not None:
                        data = self.rule_actions[(ntid, rule_id)](data_list, repo)
                    else:
                        data = None
                    return data

                elif action[0] == Action.shift:
                    data_stack.append(token[1])
                    state_stack.append(self.goto[state][t(token[0])])
                    token = next(tokens)

                elif action[0] == Action.reduce:
                    ntid, rule_id = action[1:]
                    derives = self.rule_set.nt_rules[ntid][rule_id]
                    split_point = -pop_len(derives)
                    if split_point == 0:
                        data_list = []
                    else:
                        data_list = data_stack[split_point:]
                        data_stack = data_stack[:split_point]
                        state_stack = state_stack[:split_point]
                    # perform actions
                    if self.rule_actions[(ntid, rule_id)] is not None:
                        data = self.rule_actions[(ntid, rule_id)](data_list, repo)
                    else:
                        data = None
                    data_stack.append(data)
                    state = state_stack[-1]
                    state_stack.append(self.goto[state][nt(ntid)])
                    # else:
                    #     raise ParseError  # error
