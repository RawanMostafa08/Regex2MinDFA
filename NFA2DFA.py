import json
from regex2NFA import State,NFA
epsilon = "\u03B5"
alphanumerics = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

class DFA:
    def __init__(self):
        self.states = [] #supersets
        self.start = None
        self.accepting = []
        self.alphabets = []
        

    def set_alphabets(self,nfa:NFA):
        temp_alphabets = set()
        for state in nfa.states:
            for edge in state.out_edges:
                if edge.label != epsilon:
                    temp_alphabets.add(edge.label)

        self.alphabets = list(temp_alphabets)

    def epsilon_closure(self,states:list[State]):
        stack = states
        closure = set(states)
        
        while stack:
            s = stack.pop()
            for edge in s.out_edges:
                if edge.label == epsilon and edge.dest not in closure:
                    closure.add(edge.dest)
                    stack.append(edge.dest)
        return list(closure)

    
    def move(self,states:list[State], char:str):
        destinations = []
        for s in states:
            for edge in s.out_edges:
                if edge.label == char:
                    destinations.append(edge.dest)
        return destinations
    
    
    def remove_duplicates(self,states:list[State]):
        unique_states = []
        seen_names = set()  
        for state in states:
            if state.name not in seen_names:
                seen_names.add(state.name)  
                unique_states.append(state)  
        return unique_states 
    
    def rename_states(self,transitions):
        renamed_transitions = {}
        states_map={}
        i=0
        for state in transitions:
            if state == "startingState":
                continue
            states_map[state] = "S"+str(i)
            i+=1
        
        for state in transitions:
            if state == "startingState":
                renamed_transitions["startingState"] = states_map[transitions["startingState"]]
                continue
            renamed_transitions[states_map[state]] = {}
            for edge in transitions[state]:
                if edge == "isTerminatingState" :
                    renamed_transitions[states_map[state]]["isTerminatingState"] = transitions[state]["isTerminatingState"]
                    continue
                renamed_transitions[states_map[state]][edge] = states_map[transitions[state][edge]]
        
        return renamed_transitions,states_map
    
    
    
    def NFA2DFA(self,nfa:NFA):
        self.set_alphabets(nfa)
        start = self.epsilon_closure([nfa.start])
        self.states.append(start)
        self.start = start
        for s in start:
            if s == nfa.accepting:
                self.accepting.append(start)
                break
            
        
        transitions ={}
        start_string = " ".join(sorted([s.name for s in self.start]))
        transitions["startingState"]= start_string

        unvisited = [start]
        while unvisited:
            state_list = unvisited.pop()
            for alphabet in self.alphabets:
                destinations = self.move(state_list,alphabet)
                if not destinations:
                    continue
                closure = self.epsilon_closure(destinations)
            
                for s in closure:
                    if s == nfa.accepting:
                        self.accepting.append(closure)
                        break

                if closure not in self.states:
                    self.states.append(closure)
                    unvisited.append(closure)
                
                from_state_string = " ".join(sorted([s.name for s in state_list]))
                to_state_string = " ".join(sorted([s.name for s in closure]))
            
                
                if from_state_string not in transitions:
                    transitions[from_state_string] = {}

                transitions[from_state_string][alphabet] = to_state_string
                transitions[from_state_string]["isTerminatingState"] = state_list in self.accepting

  
        for state in self.accepting:
            state_string=" ".join(sorted([s.name for s in state]))
            if state_string not in transitions:
                transitions[state_string] = {}
                transitions[state_string]["isTerminatingState"]=True
                

        renamed_transitions,states_map = self.rename_states(transitions)
        for i,state in enumerate(self.states):
            self.states[i] = State(states_map[" ".join(sorted([s.name for s in state]))])
        
        for i,state in enumerate(self.accepting):
            self.accepting[i] = State(states_map[" ".join(sorted([s.name for s in state]))])
            
        self.states = self.remove_duplicates(self.states)
        self.accepting = self.remove_duplicates(self.accepting)
        
        
        
        return transitions,renamed_transitions
    
            
            
    def to_json(self,transitions:dict,renamed_transitions:dict):
        with open("DFA_transitions.json", "w") as json_file:
            json.dump(transitions, json_file, indent=4, ensure_ascii=False)
        
        with open("DFA_transitions_renamed.json", "w") as json_file:
            json.dump(renamed_transitions, json_file, indent=4, ensure_ascii=False)
