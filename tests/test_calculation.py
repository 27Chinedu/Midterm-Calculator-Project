from datetime import datetime, timedelta
import pytest

from app.calculation import Calculation


def test_init_sets_attributes_and_default_timestamp():
	before = datetime.now() - timedelta(seconds=1)
	c = Calculation(operation='+', operand1=1, operand2=2, result=3)
	after = datetime.now() + timedelta(seconds=1)

	assert c.operation == '+'
	assert c.operand1 == 1
	assert c.operand2 == 2
	assert c.result == 3
	# timestamp should be set automatically and fall between before and after
	assert isinstance(c.timestamp, datetime)
	assert before <= c.timestamp <= after


def test_str_and_repr_contain_expected_information():
	c = Calculation('*', 3, 4, 12)
	s = str(c)
	r = repr(c)

	assert s == '3 * 4 = 12'
	# repr should contain class name and key fields
	assert 'Calculation(' in r
	assert "operation='*'" in r
	assert 'operand1=3' in r
	assert 'operand2=4' in r
	assert 'result=12' in r


def test_to_dict_serializes_timestamp_isoformat_and_fields():
	c = Calculation('-', 5.5, 2.2, 3.3)
	d = c.to_dict()

	assert set(d.keys()) == {'operation', 'operand1', 'operand2', 'result', 'timestamp'}
	assert d['operation'] == '-'
	assert float(d['operand1']) == pytest.approx(5.5)
	assert float(d['operand2']) == pytest.approx(2.2)
	assert float(d['result']) == pytest.approx(3.3)
	# timestamp should be an ISO formatted string that can be parsed back
	parsed = datetime.fromisoformat(d['timestamp'])
	assert isinstance(parsed, datetime)


def test_from_dict_reconstructs_calculation_with_mixed_types():
	now = datetime.now()
	data = {
		'operation': '^',
		'operand1': '2',          # string that can be cast to float
		'operand2': 3,            # int
		'result': '8.0',          # string float
		'timestamp': now.isoformat()
	}

	c = Calculation.from_dict(data)
	assert c.operation == '^'
	assert isinstance(c.operand1, float) and c.operand1 == 2.0
	assert isinstance(c.operand2, float) and c.operand2 == 3.0
	assert isinstance(c.result, float) and c.result == 8.0
	# timestamp parsed back correctly
	assert c.timestamp == datetime.fromisoformat(data['timestamp'])


def test_from_dict_missing_timestamp_raises_keyerror():
	data = {'operation': '+', 'operand1': 1, 'operand2': 2, 'result': 3}
	with pytest.raises(KeyError):
		Calculation.from_dict(data)


def test_from_dict_invalid_timestamp_raises_valueerror():
	data = {
		'operation': '/',
		'operand1': 4,
		'operand2': 2,
		'result': 2,
		'timestamp': 'not-a-valid-timestamp'
	}
	with pytest.raises(ValueError):
		Calculation.from_dict(data)

