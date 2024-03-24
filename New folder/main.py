import csv
import openai
import pandas as pd

# Load your OpenAI API key
openai.api_key = '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'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

def suggest_plant(temperature, soil_moisture, humidity):
    conditions = f"{temperature}°C temperature, {soil_moisture}% soil moisture, {humidity}% humidity"
    prompt = f"I have a dataset of crops with their ideal conditions. Based on the following conditions: {conditions}, I suggest growing the following crops:"
    for _, row in df.iterrows():
        temp_range = list(map(int, row['Temperature'].split('-')))
        moisture_range = list(map(int, row['Soil Moisture'].split('-')))
        humidity_range = list(map(int, row['Humidity'].split('-')))
        if temp_range[0] <= temperature <= temp_range[1] \
                and moisture_range[0] <= soil_moisture <= moisture_range[1] \
                and humidity_range[0] <= humidity <= humidity_range[1]:
            prompt += f"\n- {row['crop']}"

    response = openai.Completion.create(
        engine="text-davinci",  # Use "text-davinci" instead of "text-davinci-003"
        prompt=prompt,
        max_tokens=150
    )
    suggestions = response.choices[0].text.strip()
    return suggestions

# Example usage
temperature = int(input("Enter temperature (°C): "))
soil_moisture = int(input("Enter soil moisture (%): "))
humidity = int(input("Enter humidity (%): "))

suggested_plants = suggest_plant(temperature, soil_moisture, humidity)

if suggested_plants:
    print("Based on the conditions provided, the suggested plant(s) are:")
    print(suggested_plants)
else:
    print("No plant matches the given conditions.")
