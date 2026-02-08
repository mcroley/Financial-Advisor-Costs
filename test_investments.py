import unittest
import math


class InvestmentCalculator:
    """Helper class to encapsulate investment calculations"""
    
    def __init__(self, initial_value, fee_percentage, years, annual_return):
        self.initial_value = initial_value
        self.fee_percentage = fee_percentage
        self.years = years
        self.annual_return = annual_return
    
    def future_value_no_fees(self):
        """Calculate portfolio value without fees (just compounding growth)"""
        return self.initial_value * (1 + self.annual_return) ** self.years
    
    def future_value_with_fees(self):
        """Calculate portfolio value with annual fees deducted"""
        portfolio_value = self.initial_value
        for year in range(self.years):
            portfolio_value *= (1 + self.annual_return - self.fee_percentage)
        return portfolio_value
    
    def total_fees_paid(self):
        """Calculate total fees paid"""
        return self.future_value_no_fees() - self.future_value_with_fees()
    
    def opportunity_cost(self):
        """Calculate opportunity cost (same as total fees paid)"""
        return self.future_value_no_fees() - self.future_value_with_fees()


class TestInvestmentCalculator(unittest.TestCase):
    """Unit tests for investment calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.default_params = {
            'initial_value': 2_000_000,
            'fee_percentage': 0.01,
            'years': 15,
            'annual_return': 0.05
        }
    
    def test_future_value_no_fees_default(self):
        """Test future value without fees with default parameters"""
        calc = InvestmentCalculator(**self.default_params)
        expected = 2_000_000 * (1.05 ** 15)
        self.assertAlmostEqual(calc.future_value_no_fees(), expected, places=2)
    
    def test_future_value_with_fees_default(self):
        """Test future value with fees with default parameters"""
        calc = InvestmentCalculator(**self.default_params)
        # Manual calculation for verification
        value = 2_000_000
        for _ in range(15):
            value *= (1.05 - 0.01)  # 1.04
        expected = value
        self.assertAlmostEqual(calc.future_value_with_fees(), expected, places=2)
    
    def test_total_fees_paid_default(self):
        """Test total fees calculation with default parameters"""
        calc = InvestmentCalculator(**self.default_params)
        fees = calc.total_fees_paid()
        # Fees should be positive (cost of fees)
        self.assertGreater(fees, 0)
        # Total fees should be significant (roughly $556k)
        self.assertGreater(fees, 500_000)
        self.assertLess(fees, 600_000)
    
    def test_opportunity_cost_equals_total_fees(self):
        """Test that opportunity cost equals total fees paid"""
        calc = InvestmentCalculator(**self.default_params)
        self.assertAlmostEqual(
            calc.opportunity_cost(),
            calc.total_fees_paid(),
            places=10
        )
    
    def test_zero_years(self):
        """Test with zero years of investment"""
        calc = InvestmentCalculator(1_000_000, 0.01, 0, 0.05)
        # After 0 years, value should equal initial value
        self.assertAlmostEqual(calc.future_value_no_fees(), 1_000_000, places=2)
        self.assertAlmostEqual(calc.future_value_with_fees(), 1_000_000, places=2)
        self.assertAlmostEqual(calc.total_fees_paid(), 0, places=2)
    
    def test_zero_return(self):
        """Test with zero annual return"""
        calc = InvestmentCalculator(1_000_000, 0.01, 10, 0)
        # With 0% return and 1% fees, should lose money each year
        final_value = calc.future_value_with_fees()
        self.assertLess(final_value, 1_000_000)
        # After 10 years with 1% annual fee: 1,000,000 * (0.99^10)
        expected = 1_000_000 * (0.99 ** 10)
        self.assertAlmostEqual(final_value, expected, places=2)
    
    def test_zero_fees(self):
        """Test with zero fees"""
        calc = InvestmentCalculator(1_000_000, 0, 10, 0.05)
        # With no fees, both should be identical
        self.assertAlmostEqual(
            calc.future_value_no_fees(),
            calc.future_value_with_fees(),
            places=5
        )
        self.assertAlmostEqual(calc.total_fees_paid(), 0, places=5)
    
    def test_fees_less_than_no_fees(self):
        """Test that portfolio with fees is always less than without fees"""
        calc = InvestmentCalculator(**self.default_params)
        self.assertLess(calc.future_value_with_fees(), calc.future_value_no_fees())
    
    def test_different_initial_values(self):
        """Test with various initial investment amounts"""
        test_cases = [100_000, 500_000, 1_000_000, 5_000_000]
        
        for initial in test_cases:
            calc = InvestmentCalculator(initial, 0.01, 15, 0.05)
            # Portfolio with fees should always be less than without
            self.assertLess(calc.future_value_with_fees(), calc.future_value_no_fees())
            # Scaling initial value should scale the difference
            calc2 = InvestmentCalculator(initial * 2, 0.01, 15, 0.05)
            # The fee difference scales roughly proportionally
            ratio1 = calc.total_fees_paid() / calc.future_value_no_fees()
            ratio2 = calc2.total_fees_paid() / calc2.future_value_no_fees()
            self.assertAlmostEqual(ratio1, ratio2, places=3)
    
    def test_different_fee_percentages(self):
        """Test with various fee percentages"""
        test_fees = [0.001, 0.005, 0.01, 0.02, 0.05]
        previous_fees = 0
        
        for fee in test_fees:
            calc = InvestmentCalculator(2_000_000, fee, 15, 0.05)
            total_fees = calc.total_fees_paid()
            # Higher fees should result in higher total fees
            self.assertGreaterEqual(total_fees, previous_fees)
            previous_fees = total_fees
    
    def test_different_time_horizons(self):
        """Test with various time periods"""
        test_years = [1, 5, 10, 20, 30]
        previous_fees = 0
        
        for years in test_years:
            calc = InvestmentCalculator(2_000_000, 0.01, years, 0.05)
            total_fees = calc.total_fees_paid()
            # More years should result in higher total fees
            self.assertGreaterEqual(total_fees, previous_fees)
            previous_fees = total_fees
    
    def test_different_returns(self):
        """Test with various annual returns"""
        test_returns = [0.01, 0.03, 0.05, 0.07, 0.10]
        previous_no_fees = 0
        
        for annual_return in test_returns:
            calc = InvestmentCalculator(2_000_000, 0.01, 15, annual_return)
            future_no_fees = calc.future_value_no_fees()
            # Higher returns should result in higher future value
            self.assertGreaterEqual(future_no_fees, previous_no_fees)
            previous_no_fees = future_no_fees
    
    def test_realistic_scenario_high_fee(self):
        """Test realistic scenario with typical financial advisor fee"""
        calc = InvestmentCalculator(
            initial_value=1_000_000,
            fee_percentage=0.01,  # 1% fee (typical advisor fee)
            years=30,
            annual_return=0.07  # 7% average market return
        )
        
        future_no_fees = calc.future_value_no_fees()
        future_with_fees = calc.future_value_with_fees()
        
        # Verify reasonable values
        self.assertGreater(future_no_fees, 1_000_000)
        self.assertGreater(future_with_fees, 1_000_000)
        self.assertLess(future_with_fees, future_no_fees)
        
        # Fees should be substantial (roughly 20-25% of portfolio)
        fee_ratio = calc.total_fees_paid() / future_no_fees
        self.assertGreater(fee_ratio, 0.15)
        self.assertLess(fee_ratio, 0.35)
    
    def test_negative_return_scenario(self):
        """Test with negative returns (market downturn)"""
        calc = InvestmentCalculator(1_000_000, 0.01, 5, -0.05)
        
        # With negative returns and fees, portfolio should shrink
        final_value = calc.future_value_with_fees()
        self.assertLess(final_value, 1_000_000)
        # Fees on top of losses should make it worse
        final_no_fees = calc.future_value_no_fees()
        self.assertLess(final_value, final_no_fees)
    
    def test_break_even_fee_vs_no_fee(self):
        """Test that fee scenario never breaks even with higher initial value"""
        # If annual_return > fee_percentage, portfolio still grows
        calc = InvestmentCalculator(1_000_000, 0.01, 10, 0.05)
        self.assertGreater(calc.future_value_with_fees(), 1_000_000)
    
    def test_very_small_fee(self):
        """Test with very small fees (basis points)"""
        calc = InvestmentCalculator(1_000_000, 0.0001, 20, 0.05)  # 1 basis point
        
        # Even small fees compound over time
        fees = calc.total_fees_paid()
        self.assertGreater(fees, 0)
        # But should be small compared to higher fees
        calc_high_fee = InvestmentCalculator(1_000_000, 0.01, 20, 0.05)
        self.assertLess(fees, calc_high_fee.total_fees_paid())


if __name__ == '__main__':
    unittest.main()
