import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

# Setup
companies = ["Doc", "Grumpy", "Happy", "Sleepy", "Bashful", "Sneezy", "Dopey"]
months = pd.date_range(start="2020-01-01", periods=60, freq='M')

# Event types
news_events = [
    ("Positive Earnings Report", 0.10),
    ("Scandal Exposed", -0.15),
    ("New Tech Launched", 0.15),
    ("Regulation Hit", -0.10),
    ("Market Crash", -0.20),
    ("Buyout Rumors", 0.20)
]

# Price simulation
np.random.seed(42)
base_prices = {c: random.uniform(100, 500) for c in companies}
price_data = []
event_data = []

for date in months:
    prices = {}
    monthly_event = random.choice(companies + [None])
    event_info = ""
    for company in companies:
        last_price = base_prices[company] if len(price_data) == 0 else price_data[-1][company]
        change = np.random.normal(0, 0.05)
        if company == monthly_event:
            event = random.choice(news_events)
            change += event[1]
            event_info = f"{company}: {event[0]} ({event[1]*100:+.1f}%)"
        new_price = max(10, last_price * (1 + change))
        prices[company] = round(new_price, 2)
    price_data.append(prices)
    event_data.append((date.strftime("%b %Y"), event_info))

# Convert to DataFrame
df_prices = pd.DataFrame(price_data, index=months)
df_events = pd.DataFrame(event_data, columns=["Date", "Event"])

# Plot stock prices
plt.figure(figsize=(14, 7))
for c in companies:
    plt.plot(df_prices.index, df_prices[c], label=c)
plt.title("Stock Price Simulation (2020-2024)")
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Game initialization
cash = 1_000_000
portfolio = {c: 0 for c in companies}

# Start simulation (first 12 months, can expand to 60)
for i in range(12):
    date = df_prices.index[i]
    print(f"\n📅 {date.strftime('%b %Y')}")
    print("📈 Prices:")
    for c in companies:
        print(f"  {c}: ₹{df_prices.loc[date, c]}")
    if df_events.loc[i, 'Event']:
        print(f"📰 News: {df_events.loc[i, 'Event']}")
    
    print(f"\n💰 Cash: ₹{cash}")
    print("📦 Portfolio:", portfolio)

    for c in companies:
        action = random.choice(["buy", "sell", "hold"])  # Replace with input() for real interaction
        price = df_prices.loc[date, c]
        if action == "buy":
            qty = random.randint(1, 5)
            if cash >= qty * price:
                cash -= qty * price
                portfolio[c] += qty
        elif action == "sell":
            qty = random.randint(1, portfolio[c])
            cash += qty * price
            portfolio[c] -= qty

# Final summary
last_date = df_prices.index[11]
total_value = cash + sum(df_prices.loc[last_date, c] * portfolio[c] for c in companies)
print("\n🎯 Final Portfolio:")
for c in companies:
    print(f"{c}: {portfolio[c]} shares @ ₹{df_prices.loc[last_date, c]:.2f}")
print(f"💼 Final Value: ₹{total_value:.2f}")
print(f"📈 Net Profit/Loss: ₹{total_value - 1_000_000:.2f}")

