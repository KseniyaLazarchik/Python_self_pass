from datetime import datetime

# File to store the records
FILE_NAME = 'news_feed.txt'


class Record:
    """Base class for all records."""
    def __init__(self, text):
        self.text = text
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def publish(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def _write_to_file(self, record):
        with open(FILE_NAME, 'a') as file:
            file.write(record)


class News(Record):
    """Class for News records."""
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def publish(self):
        record = f"News|{self.date}|{self.city}|{self.text}\n"
        self._write_to_file(record)
        return record  # Return the record for reporting


class PrivateAd(Record):
    """Class for Private Ad records."""
    def __init__(self, text, expiration_date_str):
        super().__init__(text)
        self.expiration_date_str = expiration_date_str
        self.days_left = self.calculate_days_left()

    def calculate_days_left(self):
        expiration_date = datetime.strptime(self.expiration_date_str, '%Y-%m-%d')
        today = datetime.now()
        return (expiration_date - today).days

    def publish(self):
        record = f"Private Ad|{self.date}|{self.expiration_date_str}|{self.days_left} days left|{self.text}\n"
        self._write_to_file(record)
        return record  # Return the record for reporting


class UniqueRecord(Record):
    """Class for unique records."""
    def __init__(self, record_type, data):
        super().__init__(data)
        self.record_type = record_type

    def publish(self):
        record = f"{self.record_type}|{self.date}|{self.text}\n"
        self._write_to_file(record)
        return record  # Return the record for reporting


def main():
    """Main function to interact with the user and handle their input."""
    # List to keep track of records added during the session
    records = []

    while True:
        print("\nSelect the type of record you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Unique Record")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            text = input("Enter the news text: ")
            city = input("Enter the city: ")
            news_record = News(text, city)
            record = news_record.publish()
            records.append(record)

        elif choice == '2':
            text = input("Enter the ad text: ")
            expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
            private_ad_record = PrivateAd(text, expiration_date_str)
            record = private_ad_record.publish()
            records.append(record)

        elif choice == '3':
            record_type = input("Enter the type of unique record: ")
            data = input("Enter the data for the unique record: ")
            unique_record = UniqueRecord(record_type, data)
            record = unique_record.publish()
            records.append(record)

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

    # Print results of all records added during the session
    print(f"Summary of records added:")
    for record in records:
        print(record.strip())


if __name__ == "__main__":
    main()
