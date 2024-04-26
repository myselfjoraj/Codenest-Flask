class UserModel:
    def __init__(self, username, password, email, first_name, last_name,
                 city, gender, dob, martial_status, age, number, url):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.gender = gender
        self.dob = dob
        self.martial_status = martial_status
        self.age = age
        self.number = number
        self.url = url

    @staticmethod
    def from_tuple(data_tuple):
        return UserModel(*data_tuple)
