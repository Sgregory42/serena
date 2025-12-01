import gleam/int
import gleam/io
import test_repo/math
import test_repo/user

pub fn main() -> Nil {
  io.println("Hello from test_repo!")

  let alice: user.User = user.new_user("Alice", 30)
  io.println(user.format_user(alice))

  let toto = user.new_user("Toto", 30)
  io.println(user.format_user(toto))

  let result = math.add(5, 3)
  io.println("5 + 3 = " <> int.to_string(result))
}

pub fn greet(name: String) -> String {
  "Hello, " <> name <> "!"
}
