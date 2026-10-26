import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Temperature": [28, 32, 35, 30, 27],
    "Humidity": [60, 55, 45, 70, 80]
})

df.loc[len(df)] = ["Sat", 33, 50]

print("Average Temperature:", df["Temperature"].mean())
print("Minimum Temperature:", df["Temperature"].min())
print("Maximum Temperature:", df["Temperature"].max())

i = df["Temperature"].idxmax()
print("Hottest Day:", df.loc[i, "Day"])

plt.plot(df["Day"], df["Temperature"], marker="o")
plt.title("Daily Temperature Change")
plt.xlabel("Day")
plt.ylabel("Temperature")
plt.tight_layout()
plt.show()

plt.scatter(df["Humidity"], df["Temperature"])
plt.title("Humidity vs Temperature")
plt.xlabel("Humidity")
plt.ylabel("Temperature")
plt.tight_layout()
plt.show()

plt.hist(df["Temperature"], bins=5)
plt.title("Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
