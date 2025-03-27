import json
from NFA2DFA import DFA
from regex2NFA import State
class MinimizedDFA:
    def __init__(self, dfa: DFA, transitions: dict):
        self.dfa = dfa
        self.transitions = transitions
        self.minimized_transitions = {}
        
    def __difference(self, states_a: list[State], states_b: list[State]):
        names_b = {state.name for state in states_b}  
        return [state for state in states_a if state.name not in names_b]  
    
    def __split(self,group: list[State],partition: list[list[State]]): 
    # If all states in the group go to the same subgroup for all inputs, don't split
    # Otherwise, split into subgroups where states have identical transition behavior

        subgroups = {}  # key: tuple of destination groups, value: list of states
                        # ex: {(0, 1): [A, B], (1, 0): [C, D]}

        for state in group:
            destination_groups = []

            for input in self.dfa.alphabets:
                next_state = self.transitions.get(state.name, {}).get(input, None)
                destination_groups.append(next_state)
                for i, existing_group in enumerate(partition):
                    if next_state in existing_group:
                        destination_groups.append(i)
                        break
            
            
            if tuple(destination_groups) not in subgroups:
                subgroups[tuple(destination_groups)] = []
            subgroups[tuple(destination_groups)].append(state)

        # return true if a split happens, false if no split
        if len(subgroups) > 1:
            return subgroups.values(),True
        return [group],False

            
    def minimize(self):
        # inital partition TT
        non_accepting = self.__difference(self.dfa.states,self.dfa.accepting) # {A, B, C, D}  non accepting states
        accepting = self.dfa.accepting # {E}  accepting states
        if len(non_accepting)==0:
            partitions = [accepting]
        else:
            partitions = [non_accepting, accepting] #TTnew =TT = {A, B, C, D} {E}
        # partition is a list of lists(groups) 
        changed = True
        while changed:
            changed = False
            new_partitions = []

            for group in partitions:  
                subgroups, is_split = self.__split(group, partitions)
                if is_split:
                    changed = True
                new_partitions.extend(subgroups)

            partitions = new_partitions
            
                
        state_map = {}  
        minimized_states = []
        minimized_accepting = []
        minimized_transitions = {}

        # rename groups (to be one state) and check on accepting states
        for i,group in enumerate(partitions):
            new_state = f"S{i}"
            minimized_states.append(new_state)
            state_map[frozenset(group)] = new_state

            if any(state in self.dfa.accepting for state in group):
                minimized_accepting.append(new_state)

        
        # build transitions dict after minimization
        for group in partitions:
            from_state = state_map[frozenset(group)]
            minimized_transitions[from_state] = {}
            sample_state = group[0]

            for input in self.dfa.alphabets:
                next_state = self.transitions.get(sample_state.name, {}).get(input, None)

                if next_state:
                    for group2 in partitions:
                        for state in group2:
                            if next_state == state.name :
                                minimized_transitions[from_state][input] = state_map[frozenset(group2)]
                                break


        # add accept states
        for state in minimized_states:
            if state in minimized_accepting:
                minimized_transitions[state]["isTerminatingState"] = True
            else:
                minimized_transitions[state]["isTerminatingState"] = False
                
        
        # add start state
        start_state = self.transitions["startingState"]
        for group in partitions:
            for state in group:
                if start_state == state.name:
                    minimized_transitions["startingState"] = state_map[frozenset(group)]
                    break


        # minimized_transitions["startingState"] = self.transitions["startingState"]
                    
        self.dfa.states = minimized_states
        self.dfa.accepting = minimized_accepting
        self.minimized_transitions = minimized_transitions

        return minimized_transitions

    def to_json(self):
        with open("MinimizedDFA.json", "w") as json_file:
            json.dump(self.minimized_transitions, json_file, indent=4, ensure_ascii=False)
