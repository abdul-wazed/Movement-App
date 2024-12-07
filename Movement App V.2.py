import json
import random
import string
import requests
from datetime import datetime


# User defination class
class User:
    def __init__(self, first_name, last_name, dob, gender, email):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.dob = dob
        self.gender = gender.upper()
        self.email = email.lower()
        self.username = email
        self.password = None
        self.registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_password(self, password):
        self.password = password

    def display_user_info(self):
        return {
            "Full Name": f"{self.first_name} {self.last_name}",
            "Email": self.email,
            "Date of Birth": self.dob,
            "Gender": self.gender,
            "Username": self.username,
        }


# File handling function
def save_to_file(data, filename="user_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error saving data:", e)


def load_from_file(filename="user_data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print("Error loading data:", e)
        return {}


# Other functions
def validate_email(email):
    return "@" in email and "." in email


def calculate_age(dob):
    try:
        birth_date = datetime.strptime(dob, "%d-%m-%Y")
        today = datetime.now()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except ValueError:
        return -1


def generate_random_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_default_password(first_name, last_name, dob):
    return f"{first_name[:3].lower()}{last_name[:3].lower()}{dob[:2]}"


def fetch_country_capital(country_name):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        if response.status_code == 200:
            country_data = response.json()
            return country_data[0]["capital"][0] if "capital" in country_data[0] else "Capital not found."
        else:
            return "Country not found. Please check the spelling."
    except Exception as e:
        return f"Error fetching data: {e}"


def fetch_country_by_city(city_name):
    try:
        # OpenCage Geocoding API or similar can be used here for city lookups.
        api_key = "78b2c5b1e03147aea7ec5bfa797cce35"
        url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                country = data["results"][0]["components"].get("country")
                return f"The city {city_name.title()} is in {country}." if country else "Country not found."
            else:
                return "City not found. Please check the spelling."
        else:
            return "Error fetching data from the API."
    except Exception as e:
        return f"Error fetching data: {e}"


# Explore More Menu
def explore_more_menu():
    while True:
        print("\nDo you want to explore More?")
        print("1. Want to know the capital of a country?")
        print("2. Want to know the country name of a city?")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            country = input("Enter the name of the country: ")
            capital = fetch_country_capital(country)
            print(f"The capital of {country.title()} is: {capital}")
        elif choice == "2":
            city = input("Enter the name of the city: ")
            country = fetch_country_by_city(city)
            print(country)
        elif choice == "0":
            print("Thank you! Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

# Main Menu
def main_menu():
    users = load_from_file()

    while True:
        print("\nMain Menu")
        print("1. Registration")
        print("2. Check my login info")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nIf you are above 18 years of age, you can register.")
            print("1. Continue to Registration")
            print("2. Exit")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                dob = input("Enter Date of Birth (DD-MM-YYYY): ")
                age = calculate_age(dob)

                if age < 0:
                    print("Insert your date of birth in correct format.")
                    continue
                elif age < 18:
                    print("Sorry! You are not eligible for this service.")
                    continue

                gender = input("Enter Gender (M or F): ")
                email = input("Enter Email ID: ")

                if not validate_email(email):
                    print("Invalid email ID.")
                    continue

                user = User( first_name, last_name, dob, gender, email)
                print("\nPassword Menu")
                print("1. Create Random Password; 8 digits alpha-numeric random password.")
                print("2. Use Default Password; part of your name and date of birth.")
                pwd_choice = input("Enter your choice: ")

                if pwd_choice == "1":
                    password = generate_random_password()
                elif pwd_choice == "2":
                    password = generate_default_password(first_name, last_name, dob)
                else:
                    print("Invalid choice. Using random password.")
                    password = generate_random_password()

                user.set_password(password)
                users[email] = user.__dict__
                save_to_file(users)
                print("Registration successful! Your user name is", email, "and password is:", password)

                # Post-registration menu
                print("\nDo you want to Explore more?")
                print("1. Yes")
                print("0. Exit")
                explore_choice = input("Enter your choice: ")
                if explore_choice == "1":
                    explore_more_menu()
                elif explore_choice == "0":
                    print("Thank you! Exiting the application.")
                    break

            elif sub_choice == "2":
                print("Thank you.")
                break

        elif choice == "2":
            email = input("Enter your Email ID: ")
            dob = input("Enter your Date of Birth (DD-MM-YYYY): ")

            if email in users and users[email]["dob"] == dob:
                print("Welcome to the Movement App")
                print(f"Your Name is {users[email]['first_name']} {users[email]['last_name']}")
                print(f"Your user name is {email} and Password: {users[email]['password']}")

                explore_more_menu()
            else:
                print("You have entered wrong credentials or you are not a registered user of Movement App.")

        elif choice == "0":
            print("Thank you! Exiting the application.")
            break
        else:
            print("Invalid choice. Try again.")

main_menu()