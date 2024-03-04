// input and output library from standard library
use std::io;
// by default rust has a set of items defined in the standard library which it brings into the
// scope of everything. This set is called the prelude
// if a type you want to use isn't in the prelude, then you have to bring it into scope using a
// `use` statement.

//main function; the entrypoint of every rust program
fn main() {
//fn syntax declares a new function; the parenthesis showparameteres (the lack of in this case)and
//the curly braces contain the function body

    // println! is a macro to print to stdo
    println!("Guess the number!");
    println!("Please input your guess:");

    // create a variable using the let statement
    // by default variables are immutable, so we have to explicitly say that its mutable with mut
    let mut guess = String::new();
    //string is a type provided in the standard library that is 'growable', UTF-8 encoded bit of
    //text
    // :: syntax in ::new indicates that the new is an associated funtion of the String type.
    // an associated function is a function that's implemented on a type
    io:stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");
    println!("You guessed: {guess}");
}
