from collections import UserDict
import datetime


def input_error(func):
    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Please try again and add all nessesary arguments, or delete extra arguments."

        except KeyError:
            return "Invalid contact name. Please try again."

        except IndexError:
            return "Contact not found."

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    # return the value of the field as a string
    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)

        # check if the phone number contains 10 digits
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "Invalid phone number. It must be 10 digits. Please try again."
            )


class Birthday(Field):
    def __init__(self, value: str):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone, new_phone):
        self.phones[self.phones.index(phone)] = new_phone

    def find_phone(self, phone):
        # return phone
        return self.phones[self.phones.index(phone)]

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def show_birthday(self, name):
        print(f"{name}'s birthday is {self.birthday.value}")

    def birthdays(self, name):
        AddressBook.birthdays(name)

    def __str__(self) -> str:
        return f"Contact name: {self.name}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record

    def find(self, name) -> Record:
        try:
            return self.data[name]
        except KeyError:
            return None

    def delete(self, name):
        del self.data[name]

    def birthdays(self) -> list:
        """Function to get upcoming birthdays within 7 days from given list of dictionaries
        and return a list of dictionaries with name and congratulation date
        Congratulation date is set to the next working day if birthday is on Saturday or Sunday
        """
        users = self.data
        upcoming_birthdays = []  # return list

        for user in users:
            bday_user = {}  # dictionary for each iteration
            birthday = datetime.datetime.strptime(
                user["birthday"], "%Y.%m.%d"
            ).date()  # convert string to date

            today = datetime.date.today()  # get today's date

            if (
                birthday.replace(year=today.year) < today
            ):  # check if birthday has already passed
                bday_this_year = birthday.replace(
                    year=today.year + 1
                )  # if yes, set next year's birthday
            else:
                bday_this_year = birthday.replace(
                    year=today.year
                )  # if no, set this year's birthday

            # check if birthday is 29 February and this year is not a leap year
            if (
                birthday.month == 2
                and birthday.day == 29
                and not (
                    today.year % 4 == 0
                    and (today.year % 100 != 0 or today.year % 400 == 0)
                )
            ):
                bday_this_year = bday_this_year.replace(
                    day=28
                )  # set birthday to 28th February

            if bday_this_year - today <= datetime.timedelta(
                days=7
            ):  # check if birthday is within 7 days

                if bday_this_year.weekday() == 5:  # check if birthday is on Saturday
                    congratulation_date = bday_this_year + datetime.timedelta(days=2)

                elif bday_this_year.weekday() == 6:  # check if birthday is on Sunday
                    congratulation_date = bday_this_year + datetime.timedelta(days=1)

                else:  # if birthday is on any other day
                    congratulation_date = bday_this_year

                bday_user["name"] = user["name"]  # add name and birthday to dictionary
                bday_user["congratulation_date"] = congratulation_date.strftime(
                    "%Y.%m.%d"
                )
                upcoming_birthdays.append(bday_user)  # append dictionary to list
        return upcoming_birthdays


def main():
    """
    The function is controlling the cycle of command processing.
    """
    print("Welcome to the assistant bot!")
    book = AddressBook()
    while True:
        # Getting the input from the user
        user_input = input("\nEnter a command: ")
        command, *args = parse_input(user_input)

        # Checking the command and calling the appropriate function
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone(args, book))

        elif command == "all":
            all(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            birthdays(book)

        # if the command is not recognized - print an error message
        else:
            print("Invalid command.")


def parse_input(user_input) -> tuple:
    """Function is finding a command in the input and returns it"""
    # Splitting the input into words, first word is a command, other words are arguments
    cmd, *args = user_input.split()
    # Converting the command to lower case and deleting extra spaces
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    try:
        phone = Phone(phone)
    except ValueError as e:
        return str(e)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."
    else:
        record.add_phone(phone)
    return message


def change_contact(args, book: AddressBook) -> str:
    name, new_phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        return "Contact not found."
    record.add_phone(new_phone)
    return message


def phone(args, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    phone_numbers = [str(phone) for phone in record.phones]
    return f"These are the phone numbers for {name}: {', '.join(phone_numbers)}"


def all(*args) -> None:
    for name, record in AddressBook.book.data.items():
        for phone, birthday in record:
            print(f"{name}: \nPhones:{phone}, \nBirthdays: {birthday}")


def add_birthday(args, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return message


def show_birthday(args, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return f"{name}'s birthday is {record.birthday.value}"


def birthdays(book: AddressBook) -> str:
    return book.birthdays()


if __name__ == "__main__":
    main()