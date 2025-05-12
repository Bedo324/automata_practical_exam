def unary_addition(tape_input):
    tape = list(tape_input)
    head = 0
    state = 'q0'

    while state != 'q_accept':
        symbol = tape[head] if head < len(tape) else 'B' 

        if state == 'q0':
            if symbol == '1':
                head += 1
            elif symbol == '+':
                tape[head] = 'B' 
                state = 'q1'
                head += 1
            else:
                state = 'q_accept'

        elif state == 'q1':
            if head < len(tape) and tape[head] == '1':
                tape[head] = 'B'  
                state = 'q2'
                head -= 1
            else:
                state = 'q_accept'  

        elif state == 'q2':
            if head >= 0 and tape[head] == '1':
                head -= 1
            elif head >= 0 and tape[head] == 'B':
                state = 'q3'
                head += 1

        elif state == 'q3':
            if head < len(tape) and tape[head] == '1':
                head += 1
            elif head == len(tape) or tape[head] == 'B':
                tape.insert(head, '1') 
                state = 'q1'
                head += 1
                
    return ''.join([s for s in tape if s == '1'])

# Example usage:
input_tape = "111+11"
result = unary_addition(input_tape)
print("Output:", result)
