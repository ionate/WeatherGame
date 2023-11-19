import requests
import random
import os
from dotenv import load_dotenv

PFX_IMAGING = '!img'
PFX_GUESS = '!guess'
PFX_ALIENSTAR = '!as'
PFX_MAINHELP = '!help'

load_dotenv() 

API_KEY = os.getenv("WEATHERAPI_TOKEN")

CITIES = [
    "New York",
    "Los Angeles",
    "London",
    "Tokyo",
    "Sydney",
    "Berlin",
    "Paris",
    "Dubai",
]

#(float(celsius) * 9 / 5 + 32)
#lambda fahrenheit = lambda x: float(x)(9/5)+32
def get_f(celsius):
    fahrenheit = (float(celsius) * 9 / 5 + 32)
    return fahrenheit

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        return temperature
    else:
        print("Failed to fetch weather data.")
        return None

def player_guess():
    return float(input("Enter your temperature guess: "))

def ai_guess(previous_guess):
    # Simple AI strategy: Random guess within 3 degrees of the previous guess
    return random.uniform(previous_guess - 3, previous_guess + 3)

def calculate_score(actual_temp, guess):
    return max(0, 10 - abs(actual_temp - guess))

def main():
    print("Welcome to the Weather Guessing Game!")

    player_score, ai_score = 0, 0

    while True:
        selected_city = random.choice(CITIES)
        print(f"\nCity: {selected_city}")
        
        actual_temp_f = get_f(get_weather(selected_city))
        
        if actual_temp_f is None:
            continue

        player_temp_guess = player_guess()
        ai_temp_guess = ai_guess(player_temp_guess)

        print(f"AI's guess: {ai_temp_guess:.1f}")
        print(f"Actual temperature: {actual_temp_f:.1f}")

        player_score += calculate_score(actual_temp_f, player_temp_guess)
        ai_score += calculate_score(actual_temp_f, ai_temp_guess)

        print(f"Your score: {player_score}")
        print(f"AI score: {ai_score}")

        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
