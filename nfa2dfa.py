import sys

# hash cu caracterele din alfabet si un index asociat
sigma = {}

# date nfa
nfa_no_of_states = 0
nfa_final_states = []
nfa_transitions = {}

# date dfa
dfa_no_of_states = 0
dfa_final_states = []

# dictionar cu inchiderile pe epsilon ale starilor folosite
precomputed_next_states = {}




def read_input(input_path):
    input_file = open(input_path, "r")

    global nfa_no_of_states, nfa_final_states
    nfa_no_of_states = int(input_file.readline().strip())

    nfa_final_states = input_file.readline().split( )
    #print(nfa_final_states[0])


    alphabet = set()
    for line in input_file:
        line = line.strip().split()
        alphabet.add(line[1])
        nfa_transitions[(line[0], line[1])] = list(line[2:])

    compute_sigma(alphabet)
    input_file.close()




def write_output(output_path, dfa_transition, states_hash):
    output_file = open(output_path, "w+", newline='\n')
    output_file.write(str(dfa_no_of_states) + "\n")

    output_file.writelines("%s " % states_hash[dfa_final_states[i]] for i in range(0, len(dfa_final_states) - 1))
    output_file.write(states_hash[dfa_final_states[len(dfa_final_states) - 1]] + "\n")

    for trans_key, trans_value in dfa_transition.items():
        for sigma_key, sigma_value in sigma.items():
                output_file.write(states_hash[trans_key] + " " + sigma_key + " " + states_hash[trans_value[sigma_value]] + "\n")

    output_file.close()


# genereaza dictionarul pentru alfabet (caracter, index)
def compute_sigma(alphabet):
    sigma_temp = sorted(alphabet)
    counter = 0
    for symbol in sigma_temp:
        if symbol != 'eps':
            sigma[symbol] = counter
            counter += 1

# intoarce o lista de stari urmatoare cu tranzitii pe epsilon
def get_epsilon_closure(state):

    # verifica existenta unei tranzitii pe epsilon
    if not (state, 'eps') in nfa_transitions:
        return None

    visited = [False for i in range(0, nfa_no_of_states)]
    eps_closure_state = []
    state_queue = [state]
    while state_queue != []:
        top = state_queue.pop(0)
        if not top in eps_closure_state:
            eps_closure_state.append(top)
        if (top, 'eps') in nfa_transitions and (visited[int(top)] == False):
            state_queue += nfa_transitions[(top, 'eps')]
            visited[int(top)] = True

    return eps_closure_state

# intoarce starea urmatoare in functie de starea curenta si simbol
def next_step(state, symbol):
    next_state = ''
    temp_states = ''
    if (state, symbol) in nfa_transitions:
        temp_states = nfa_transitions[(state, symbol)]
        next_state = temp_states
        for state in temp_states:
            eps_closure = get_epsilon_closure(state)
            if eps_closure != None:
                next_state = next_state + eps_closure
        return ''.join(sorted(set(next_state)))
    else:
        return ''

# primeste o stare compusa (formata din mai multe stari ale nfa-ului)
# intoarce starea urmatoare
def next_step_complex(states, symbol):
    next_state = ''
    for state in states:
        if not (state, symbol) in precomputed_next_states:
            current_next_step = next_step(state, symbol)
            precomputed_next_states[(state, symbol)] = current_next_step
        else:
            current_next_step = precomputed_next_states[((state, symbol))]
        if current_next_step != [] and not set(current_next_step).issubset(set(next_state)):
            next_state += current_next_step
    return ''.join(list(sorted(set(next_state))))


def compute_dfa_transitions():
    dfa_transitions = {}
    current_state = '0'
    queue_states = []

    # calculeaza starea initiala a dfa-ului
    initial_closure = get_epsilon_closure('0')
    if initial_closure != None:
        initial_closure.append('0')
        current_state = ''.join(sorted(set(initial_closure)))
    queue_states.append(current_state)

    # se adauga in dictionar starile in care se poate ajunge din starea curenta
    while queue_states != []:
        top = queue_states.pop(0)
        dfa_transitions[top] = []
        for symbol in sigma:
            next_state = next_step_complex(top, symbol)
            dfa_transitions[top].append(next_state)
            if not next_state in dfa_transitions:
                queue_states.append(next_state)

    # calculeaza starile finale in functie de starile dfa-ului
    compute_dfa_final_states(dfa_transitions)

    return dfa_transitions

# verifica daca noile stari contin cel putin o stare finala a nfa-ului
# si le adauga la lista de stari finale
def compute_dfa_final_states(dfa_transitions):
    final_states = []
    for transition in dfa_transitions.keys():
        for fin_state in nfa_final_states:
            if fin_state in transition:
                final_states.append(transition)

    global dfa_no_of_states, dfa_final_states
    dfa_no_of_states = len(dfa_transitions)
    dfa_final_states = list(set(final_states))

# redenumeste starile dfa-ului
def convert_states(dfa_transitions):
    states_hash = {}

    state_number = 0
    for temp_key in dfa_transitions.keys():
        states_hash[temp_key] = str(state_number)
        state_number += 1

    return states_hash

def convert_to_dfa(input_path, output_path):
    # parsare fisier de intrare
    read_input(input_path)

    # calculeaza tranzitiile dfa-ului
    dfa_transitions = compute_dfa_transitions()

    # redenumeste starile dfa-ului intr-o forma mai "human readable"
    states_hash = convert_states(dfa_transitions)

    # scrie automatul obtinut in fisier
    write_output(output_path, dfa_transitions, states_hash)

if __name__ == '__main__':
    convert_to_dfa(sys.argv[1], sys.argv[2])




