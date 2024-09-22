import os
from datetime import datetime
from task_4 import fix_misspelling
from task_4 import text_normalize
from task_4 import generate_word_count_csv
from task_4 import generate_letter_count_csv

# Default file to store the records
FILE_NAME = ('news_feed.txt')
DEFAULT_INPUT_FILE = 'input_records.txt'

class Record:
    """Base class for handling records."""
    # Class-level variable to accumulate text from all records
    accumulated_text = ""

    def __init__(self, text):
        self.text = text
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def publish(self):
        """Publishes the record and updates accumulated text."""
        # Add the current record's text to the accumulated text
        Record.accumulated_text += " " + self.text

    @classmethod
    def finalize_and_update_csvs(cls):
        """Finalize the accumulated text and generate word and letter count CSVs."""
        # Call the methods to update word and letter count CSVs using accumulated text
        generate_word_count_csv(cls.accumulated_text)
        generate_letter_count_csv(cls.accumulated_text)

    def _write_to_file(self, record):
        with open(FILE_NAME, 'a') as file:
            file.write(record)


class News(Record):
    """Class for News records."""
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def publish(self):
        """Override publish method to include city information."""
        record = f"News\nDate: {self.date}\nCity: {self.city}\n{self.text}\n\n"
        self._write_to_file(record)
        super().publish()  # Accumulate the text in the Record class
        return record


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
        """Publish Private Ad record."""
        record = f"Private Ad\nDate: {self.date}\nExpires: {self.expiration_date_str}\nDays left: {self.days_left}\n{self.text}\n\n"
        self._write_to_file(record)
        super().publish()  # Accumulate the text in the Record class
        return record


class Comment(Record):
    """Class for Comment records."""
    def __init__(self, nickname, text):
        super().__init__(text)
        self.nickname = nickname
        self.words_num = self.words_count()

    def words_count(self):
        if isinstance(self.text, str):
            words = self.text.split()
            return len(words)
        else:
            return 0

    def publish(self):
        """Publish Comment record."""
        record = f"Nickname: {self.nickname}\nDate: {self.date}\n{self.text}\nWords count: {self.words_num}\n\n"
        self._write_to_file(record)
        super().publish()  # Accumulate the text in the Record class
        return record


class FileReader:
    """Class to read records from a text file and process them."""
    def __init__(self, file_path=DEFAULT_INPUT_FILE):
        self.file_path = file_path

    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist.")
            return

        with open(self.file_path, 'r') as file:
            data = file.read().strip().split('---')

        for record_data in data:
            record_lines = record_data.strip().split('\n')
            if not record_lines:
                continue
            record_type = record_lines[0].strip()
            if record_type == 'News':
                text = record_lines[1].split(':', 1)[1].strip()
                city = record_lines[2].split(':', 1)[1].strip()
                record = News(text_normalize(text), text_normalize(city))
            elif record_type == 'Private Ad':
                text = record_lines[1].split(':', 1)[1].strip()
                expiration_date_str = record_lines[2].split(':', 1)[1].strip()
                record = PrivateAd(text_normalize(text), expiration_date_str)
            elif record_type == 'Comment':
                nickname = record_lines[1].split(':', 1)[1].strip()
                text = record_lines[2].split(':', 1)[1].strip()
                text = fix_misspelling(text)
                record = Comment(text_normalize(nickname), text_normalize(text))
            else:
                print(f"Unknown record type: {record_type}")
                continue

            record.publish()
            print(f"Processed record: {record_type}")

        # Remove file after successful processing
        os.remove(self.file_path)
        print(f"File '{self.file_path}' processed and removed.")


def main():
    """Main function to interact with the user and handle their input."""
    # List to keep track of records added during the session
    records = []

    while True:
        print("\nSelect the type of record you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Comment")
        print("4. Process records from file")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

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
            nickname = input("Enter your nickname: ")
            text = input("Enter your comment: ")
            comments = Comment(nickname, text)
            record = comments.publish()
            records.append(record)

        elif choice == '4':
            file_path = input(f"Enter the file path (default: {DEFAULT_INPUT_FILE}): ").strip() or DEFAULT_INPUT_FILE
            file_reader = FileReader(file_path)
            file_reader.process_file()

        elif choice == '5':
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

Record.finalize_and_update_csvs()