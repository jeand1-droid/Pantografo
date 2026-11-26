## How it works

This project detects mechanical blockages and travel
limit faults in an X-Y cutting pantograph.

The circuit monitors movement commands, encoder pulses
and limit switches.

When a fault is detected, an alarm and a stop request
are activated until the system is reset.

## How to test

1. Apply a 10 MHz clock signal.
2. Reset the circuit using rst_n.
3. Activate a movement command.
4. Generate encoder pulses to simulate normal movement.
5. Stop the encoder pulses for at least 100 ms.
6. Verify the mechanical blockage output.
7. Reset the circuit.
8. Activate a limit switch during a movement command.
9. Verify the fault, alarm and stop outputs.

## External hardware

- Two incremental encoders.
- Four limit switches.
- External movement command signals.
- External alarm and stop interface.
