import pytest
from cpu_element import CPU_element

source = "source"
result = "result"


class Test_CPU_element:
    def test_init(self):
        with pytest.raises(TypeError):
            CPU_element()
            CPU_element(source)
            CPU_element(source, result)
            CPU_element([1], [2])
        cpu = CPU_element([source], [result])
        assert source in cpu.inputs
        assert source not in cpu.outputs
        assert result in cpu.outputs
        assert result not in cpu.inputs

    def test_connect(self):
        a = CPU_element([source], [result])
        b = CPU_element([result], [])
        with pytest.raises(TypeError):
            b.connect(a)
            b.connect(5)
            b.connect([5])
        b.connect([a])
        assert b.input_sources[result] == a
        with pytest.raises(KeyError):
            b.input_sources[source]
            b.connect([CPU_element([], [result])])
        names = "abcdefg"
        elements = [CPU_element([], [c]) for c in names]
        b.connect(elements)
        for name, element in zip(names, elements):
            assert name in b.input_sources
            assert b.input_sources[name] == element

    def test_read_input(self):
        a = CPU_element([source], [result])
        b = CPU_element([result], [])
        i = 42
        b.connect([a])
        a.outputs[result] = i
        assert b.inputs[result] == 0
        b.read_inputs()
        assert b.inputs[result] == i
        with pytest.raises(KeyError):
            a.read_inputs()
        with pytest.raises(TypeError):
            a.outputs[result] = "hei"
            b.read_inputs()

    def test_write_output(self):
        with pytest.raises(NotImplementedError):
            CPU_element([], []).write_output()
