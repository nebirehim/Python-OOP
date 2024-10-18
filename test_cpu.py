"""
Tests for CPU class
Command line: python -m pytest database/test_cpu.py
"""
import pytest
import inventory


@pytest.fixture
def cpu_values():
    return {
        'name': 'RZYEN Threadripper 2990WX',
        'manufacturer': 'NVIDIA',
        'total': 10,
        'allocated': 5,
        'cores': 32,
        'socket': '/dev/ttyUSB0',
        'power_watts': 250
    }


@pytest.fixture
def cpu(cpu_values):
    """
    Creates instance of CPU class using CPU values from cpu_value dictionary
    """
    return inventory.CPU(**cpu_values)


def test_cpu(cpu, cpu_values):
    for attr_name in cpu_values:
        assert getattr(cpu, attr_name) == cpu_values.get(attr_name)


@pytest.mark.parametrize(
    'cores,exception', [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_invalid_cores(cores, exception, cpu_values):
    cpu_values['cores'] = cores
    with pytest.raises(exception):
        inventory.CPU(**cpu_values)


@pytest.mark.parametrize(
    'watts,exception', [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_invalid_watts(watts, exception, cpu_values):
    cpu_values['power_watts'] = watts
    with pytest.raises(exception):
        assert inventory.CPU(**cpu_values)


def test_repr(cpu):
    assert cpu.category in repr(cpu)
    assert cpu.name in repr(cpu)
    assert cpu.socket in repr(cpu)
    assert str(cpu.cores) in repr(cpu)