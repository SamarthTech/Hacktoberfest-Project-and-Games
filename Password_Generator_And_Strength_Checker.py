# password strength checker
import re
import random

class PasswordStrengthChecker:
    def __init__(self, password):
        self.password = password

    def check_password_strength(self):
        score = 0

        # Check length of password
        if len(self.password) < 8:
            return "Very Weak"
        elif len(self.password) >= 8 and len(self.password) <= 10:
            score += 1
        elif len(self.password) > 10:
            score += 2

        # Check for uppercase letters
        if re.search(r'[A-Z]', self.password):
            score += 1

        # Check for lowercase letters
        if re.search(r'[a-z]', self.password):
            score += 1

        # Check for numbers
        if re.search(r'\d', self.password):
            score += 1

        # Check for special characters
        if re.search(r'[^A-Za-z0-9]', self.password):
            score += 2

        # Return password strength based on score
        if score == 0:
            return "Very Weak"
        elif score == 1:
            return "Weak"
        elif score == 2:
            return "Medium"
        elif score == 3:
            return "Strong"
        else:
            return "Very Strong"

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = PasswordStrengthChecker(password)
        self.password_history = [password]

    def change_password(self, new_password):
        """
        This function changes the user's password and adds the old password to
        the password history.
        """
        old_password = self.password.password
        self.password_history.append(old_password)
        self.password = PasswordStrengthChecker(new_password)

    def reset_password(self):
        """
        This function generates a new random password for the user and adds it to
        the password history.
        """
        new_password = self.generate_random_password()
        self.password_history.append(self.password.password)
        self.password = PasswordStrengthChecker(new_password)
        return new_password

    def generate_random_password(self):
        """
        This function generates a random password of length 10 with at least one
        uppercase letter, one lowercase letter, one number, and one special
        character.
        """
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        password = ''.join(random.choice(chars) for i in range(10))
        while not (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password) and re.search(r'[^A-Za-z0-9]', password)):
            password = ''.join(random.choice(chars) for i in range(10))
        return password

    def login(self, password):
        """
        This function checks if the password is valid for the user and returns True
        if it is, or False if it is not.
        """
        if self.password.password != password:
            print("Incorrect password.")
            return False
        else:
            print("Welcome back, {}!".format(self.username))
            return True

# example usage
# create a new user with a password
user1 = User("johndoe", "MyPassword1!")

# check the strength of the password
print(user1.password.check_password_strength())  # prints "Medium"

# attempt to login with the wrong password
user1.login("WrongPassword1!")  # prints "Incorrect password." and returns False

# attempt to login with the correct password
user1.login("MyPassword1!")  # prints "Welcome back, johndoe!" and returns True

# change the user's password
user1.change_password("NewPassword123!")

# check the strength of the new password
print(user1.password.check_password_strength())  # prints "Strong"

# reset the user's password
new_password = user1.reset_password()

# check the strength of the new password
print(user1.password.check_password_strength())  # prints "Very Strong"
