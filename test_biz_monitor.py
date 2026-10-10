from biz_monitor import calculate_profit, format_naira, calculate_total_profit, get_low_stock
import pytest

def test_calculate_profit():
    assert calculate_profit(500, 800, 20) == 6000
    assert calculate_profit(1000, 1500, 3) == 1500
    assert calculate_profit(0, 100, 1) == 100

def test_format_naira():
    assert format_naira(6000) == "₦6,000.00"
    assert format_naira(1500.5) == "₦1,500.50"

def test_calculate_total_profit():
    inventory = {
        "Garri": {"cost_price": 500, "selling_price": 800, "quantity": 20},
        "Rice": {"cost_price": 1000, "selling_price": 1500, "quantity": 3}
    }
    assert calculate_total_profit(inventory) == 7500

def test_get_low_stock():
    inventory = {
        "Garri": {"cost_price": 500, "selling_price": 800, "quantity": 20},
        "Rice": {"cost_price": 1000, "selling_price": 1500, "quantity": 3},
        "Oil": {"cost_price": 1200, "selling_price": 1800, "quantity": 2}
    }
    low = get_low_stock(inventory, 5)
    assert "Rice" in low
    assert "Oil" in low
    assert "Garri" not in low

# Run tests
pytest.main(["-v", "--tb=line", "-rN", __file__])