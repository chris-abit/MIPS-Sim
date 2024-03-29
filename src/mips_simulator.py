#!/usr/bin/env python3
from cpu_element import CPU_element
from elements import Adder, Mux, Instruction_pointer, Constant
from memory import Data_memory, Instruction_memory
from register_file import Register_file


class MIPS_simulator:
    def __init__(self):
        self.ticks = 0
        self.elements = []
        self.ip = Instruction_pointer(["Ins_incr"], ["Ins_out"])
        self.data_memory = Data_memory([], [])
        self.instruction_memory = Instruction_memory([], [])
        self.register_file = Register_file([], [])
        self.elements.append(self.ip)
        self.elements.append(Constant("Constant", 4))
        self.elements.append(Constant("Control", 1))
        self.elements.append(Adder(["Constant", "Ins_out"], ["Ins_incr"]))
        self.elements.append(Mux(["Control", "Ins_out", "Ins_incr"],
                                 ["Result"]))
        self._connect()

    def _connect(self):
        for element in self.elements:
            element.connect(self.elements)
        self.elements.remove(self.ip)

    def setup(self, file_name, startpoint):
        """ Sets a startpoint and initializes memory."""
        self.ip.inputs[self.ip.input_names[0]] = startpoint
        self.data_memory.initialize_memory(file_name)
        self.instruction_memory.initialize_memory(file_name)

    def tick(self):
        self.ip.write_outputs()
        for element in self.elements:
            element.read_inputs()
            element.write_outputs()
        self.ip.read_inputs()
        self.ticks += 1

    def status(self):
        """ Returns the status of the simulator as a printable string."""
        outputs = ["Total ticks: {}".format(self.ticks)]
        outputs.append(self.ip.status())
        outputs.append(self.register_file.status())
        outputs.append(self.data_memory.status())
        outputs.append("Result: {}"
                       .format(self.elements[-1].outputs["Result"]))
        return "\n".join(outputs)


if __name__ == "__main__":
    simulator = MIPS_simulator()
    for i in range(10):
        simulator.tick()
    print(simulator.status())
