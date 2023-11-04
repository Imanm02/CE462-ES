
module digital_lock(
    input clk,
    input rst,
    input inp,
    output reg unlocked
);

typedef enum {IDLE, FIRST_BIT, SECOND_BIT, UNLOCKED} state_t;

reg [3:0] current_state, next_state;

always @(posedge clk or posedge rst) {
    if (rst) current_state <= IDLE;
    else current_state <= next_state;
}

always @(current_state, inp) begin
    unlocked = 1'b0; // Default value for unlocked
    case(current_state)
        IDLE: begin
            if (inp == 1'b1) {
                next_state = FIRST_BIT;
            } else 
            if (inp == 1'b0) {
                next_state = IDLE;
            }
        end
        FIRST_BIT: begin
            if (inp == 1'b0) {
                next_state = SECOND_BIT;
            } else 
            if (inp == 1'b1) {
                next_state = IDLE;
            }
        end
        SECOND_BIT: begin
            if (inp == 1'b1) {
                next_state = UNLOCKED;
                unlocked = 1'b1;
            } else 
            if (inp == 1'b0) {
                next_state = IDLE;
            }
        end
        UNLOCKED: begin
        end
    endcase
end

endmodule