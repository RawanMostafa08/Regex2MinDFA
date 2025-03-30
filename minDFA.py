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

    def __split(self, group: list[State], partition: list[list[State]]):
        subgroups = {}

        for state in group:
            destination_groups = []
            for input_char in self.dfa.alphabets:
                next_state = self.transitions.get(state.name, {}).get(input_char, None)
                found = False
                for i, existing_group in enumerate(partition):
                    if any(next_state == g.name for g in existing_group):
                        destination_groups.append(i)
                        found = True
                        break
                if not found:
                    destination_groups.append(None)  

            key = tuple(destination_groups)
            if key not in subgroups:
                subgroups[key] = []
            subgroups[key].append(state)

        if len(subgroups) > 1:
            return list(subgroups.values()), True
        return [group], False

    def minimize(self):
        non_accepting = self.__difference(self.dfa.states, self.dfa.accepting)
        accepting = self.dfa.accepting
        partitions = [non_accepting, accepting] if non_accepting else [accepting]
        
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
        
        for i, group in enumerate(partitions):
            new_state = f"S{i}"
            minimized_states.append(new_state)
            state_map[tuple(sorted(state.name for state in group))] = new_state
            if any(state.name in {s.name for s in self.dfa.accepting} for state in group):
                minimized_accepting.append(new_state)
        
        for group in partitions:
            from_state = state_map[tuple(sorted(state.name for state in group))]
            minimized_transitions[from_state] = {}
            sample_state = group[0]
            
            for input_char in self.dfa.alphabets:
                next_state = self.transitions.get(sample_state.name, {}).get(input_char, None)
                if next_state:
                    for group2 in partitions:
                        if any(next_state == state.name for state in group2):
                            minimized_transitions[from_state][input_char] = state_map[tuple(sorted(state.name for state in group2))]
                            break
        
        for state in minimized_states:
            minimized_transitions[state]["isTerminatingState"] = state in minimized_accepting
        
        start_state = self.transitions.get("startingState", None)
        if start_state:
            for group in partitions:
                if any(start_state == state.name for state in group):
                    minimized_transitions["startingState"] = state_map[tuple(sorted(state.name for state in group))]
                    break
        
        self.dfa.states = minimized_states
        self.dfa.accepting = minimized_accepting
        self.minimized_transitions = minimized_transitions
        
        return minimized_transitions

    def to_json(self):
        with open("MinimizedDFA.json", "w") as json_file:
            json.dump(self.minimized_transitions, json_file, indent=4, ensure_ascii=False)
