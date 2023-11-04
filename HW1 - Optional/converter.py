import json

class FSM:
    def __init__(self, states, inputs, output, transitions, initial_state, final_state):
        self.states = states
        self.inputs = inputs
        self.output = output
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_state = final_state

def generate_verilog_from_fsm(fsm: FSM):
    num_bits = len(bin(len(fsm.states) - 1))

    verilog_code = f"""
module digital_lock(
    input clk,
    input rst,
    input inp,
    output reg {fsm.output}
);

typedef enum {{{', '.join(fsm.states)}}} state_t;

reg [{num_bits - 1}:0] current_state, next_state;

always @(posedge clk or posedge rst) {{
    if (rst) current_state <= {fsm.initial_state};
    else current_state <= next_state;
}}

always @(current_state, inp) begin
    {fsm.output} = 1'b0; // Default value for {fsm.output}
    case(current_state)"""

    for state in fsm.states:
        verilog_code += f"""
        {state}: begin"""
        
        for inp_val in fsm.inputs:
            next_state = fsm.transitions[state].get(inp_val, fsm.initial_state)
            condition = f"inp == 1'b{inp_val}" if inp_val in ['0', '1'] else inp_val
            verilog_code += f"""
            if ({condition}) {{
                next_state = {next_state};"""
            if next_state == fsm.final_state:
                verilog_code += f"""
                {fsm.output} = 1'b1;"""
            verilog_code += """
            } else """
        verilog_code = verilog_code.rstrip(" else ")
        verilog_code += f"""
            next_state = {fsm.initial_state};
        end"""

    verilog_code += """
    endcase
end

endmodule
"""
    return verilog_code

if __name__ == "__main__":
    with open("fsm.json", 'r') as file:
        fsm_data = json.load(file)
        fsm = FSM(**fsm_data)
        for state in fsm.states:
            fsm.transitions[state].pop('rst', None)
        verilog_code = generate_verilog_from_fsm(fsm)
        with open('FSM.v', 'w') as output:
            output.write(verilog_code)