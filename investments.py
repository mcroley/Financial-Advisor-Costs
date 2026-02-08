# Initial parameters
initial_value = 2_000_000  # Initial portfolio value ($2 million)
fee_percentage = 0.01  # 1% annual fee
years = 15  # Duration (15 years)
annual_return = 0.05  # Annual return (5%)

# Calculate the portfolio value without fees (just compounding growth)
future_value_no_fees = initial_value * (1 + annual_return) ** years

# Calculate the future value with fees (subtracting 1% annually)
portfolio_value_with_fees = initial_value
for year in range(years):
    portfolio_value_with_fees *= (1 + annual_return - fee_percentage)

# Calculate total fees paid
total_fees_paid = future_value_no_fees - portfolio_value_with_fees

# Calculate the opportunity cost (difference in future values)
opportunity_cost = future_value_no_fees - portfolio_value_with_fees

# Print results
print(f"Total fees paid: ${total_fees_paid:,.2f}")
print(f"Opportunity cost (lost investment): ${opportunity_cost:,.2f}")
print(f"Future value without fees: ${future_value_no_fees:,.2f}")
