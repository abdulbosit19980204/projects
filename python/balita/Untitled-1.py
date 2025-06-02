
class MyContextManagerClass:
    def __init__(self,file_path, file_mode):
        self.file_path = file_path
        self.file_mode = file_mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.file_path, 'rb')  # SQLite3 fayli uchun ikkilik rejim
        print("File opened:", self.file_path)
        print("File mode:", self.file_mode)
        print("Entering context:", self.file)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context:", self.file.name)
        self.file.close()
        # if self.file:
        #     print("Exiting context:", self.file)
        #     self.file.close()
        # if exc_type is not None:
        #     print(f"An exception occurred: {exc_value}")
        # return True

with MyContextManagerClass("db.sqlite3", "rb", ) as file:
    print("Inside context manager", file.__enter__)
    data=file.read()
    print("Fayl ma'lumotlari o'qildi", data)
    # print("".join(lines))
        