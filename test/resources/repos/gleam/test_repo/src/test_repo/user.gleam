import gleam/string

pub type User {
  User(name: String, age: Int)
}

pub fn new_user(name: String, age: Int) {
  User(name: name, age: age)
}

pub fn get_name(user: User) -> String {
  user.name
}

pub fn get_age(user: User) -> Int {
  user.age
}

pub fn format_user(user: User) -> String {
  string.concat([user.name, " is ", string.inspect(user.age), " years old"])
}

pub fn is_adult(user: User) -> Bool {
  user.age >= 18
}
