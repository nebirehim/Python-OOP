"""
Tests for Resource class
Command line: python  -m pytest database/test_resource.py
"""

import pytest
import inventory


@pytest.fixture
def resource_values():
    return {
        'name': 'Mercedes G class',
        'manufacturer': 'Mercedes Benz',
        'total': 100,
        'allocated': 50
    }


@pytest.fixture
def resource(resource_values):
    return inventory.Resource(**resource_values)


def test_resource_values(resource_values, resource):
    for attr_name in resource_values:
        assert getattr(resource, attr_name) == resource_values.get(attr_name)


def test_invalidate_total_type():
    with pytest.raises(TypeError):
        inventory.Resource('Mercedes G class', 'Mercedes Benz', 10.5, 5)


def test_invalidate_allocated_type():
    with pytest.raises(TypeError):
        inventory.Resource('Mercedes', 'Mercedes Benz', 10, 2.5)


def test_invalidate_total_value():
    with pytest.raises(ValueError):
        inventory.Resource('Mercedes', 'Mercedes Benz', -10, 0)


@pytest.mark.parametrize('total,allocated', [(10, -5), (10, 20)])
def test_invalidate_allocated_value(total, allocated):
    with pytest.raises(ValueError):
        inventory.Resource('Mercedes', 'Mercedes Benz', total, allocated)


def test_total_value(resource):
    assert resource.total == resource._total


def test_allocated_value(resource):
    assert resource.allocated == resource._allocated


def test_available_value(resource):
    assert resource.available == resource.total - resource.allocated


def test_category_value(resource):
    assert resource.category == 'resource'


def test_str_repr(resource):
    assert str(resource) == resource.name


def test_repr_repr(resource):
    assert repr(resource) == '{} ({} - {}): total={}, allocated={}'.format(
        resource.name, resource.category, resource.manufacturer, resource.total,
        resource.allocated
    )


def test_claim(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.claim(n)
    assert resource.total == original_total
    assert resource.allocated == original_allocated + n


@pytest.mark.parametrize('value', [-1, 0, 1_000])
def test_calim_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.claim(value)


def test_freeup(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.freeup(n)
    assert resource.allocated == original_allocated - n
    assert resource.total == original_total


@pytest.mark.parametrize('value', [-1, 0, 1_000])
def test_freeup_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.freeup(value)


def test_died(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.died(n)
    assert resource.total == original_total - n
    assert resource.allocated == original_allocated - n


@pytest.mark.parametrize('value', [-1, 0, 1_000])
def test_died_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.died(value)


def test_purchased(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.purchased(n)
    assert resource.total == original_total + n
    assert resource.allocated == original_allocated


@pytest.mark.parametrize('value', [-1, 0])
def test_purchased_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.purchased(value)