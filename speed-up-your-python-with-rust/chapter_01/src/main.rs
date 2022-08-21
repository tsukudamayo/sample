// fn print(input: String) {
//     println!("{}", input);
// }

use std::collections::HashMap;

enum Value {
    Str(&'static str),
    Int(i32),
}

macro_rules! capitalize {
    ($a: expr) => {
	let mut v: Vec<char> = $a.chars().collect();
	v[0] = v[0].to_uppercase().nth(0).unwrap();
	$a = v.into_iter().collect();
    }
}

struct Coordinate <T> {
    x: T,
    y: T,
}

struct Stock {
    name: String,
    open_price: f32,
    stop_loss: f32,
    take_profit: f32,
    current_price: f32,
}

impl Stock {
    fn new(stock_name: &str, price: f32) -> Stock {
	return Stock{
	    name: String::from(stock_name),
	    open_price: price,
	    stop_loss: 0.0,
	    take_profit: 0.0,
	    current_price: price,
	}
    }

    fn with_stop_loss(mut self, value: f32) -> Stock {
	self.stop_loss = value;
	return self
    }

    fn with_take_profit(mut self, value: f32) -> Stock {
	self.take_profit = value;
	return self
    }

    fn update_price(&mut self, value: f32) {
	self.current_price = value;
    }
}

trait CanTransfer {
    fn transfer_stock(&self) -> ();

    fn print(&self) -> () {
	println!("a transfer is happening");
    }
}

impl CanTransfer for Stock {
    fn transfer_stock(&self) -> () {
	println!("the stock {} is being transferred for {}", self.name, self.current_price);
    }
}

fn print(input_string: &str) {
    println!("{}", input_string);
}

fn process_enum(value: &Value) -> () {
    match value {
	Value::Str(inside_value) => {
	    println!("the following value is an str: {}", inside_value);
	}
	Value::Int(inside_value) => {
	    println!("the following value is an int: {}", inside_value);
	}
    }
}

fn alter_number(number: &mut i8) {
    *number += 1
}

fn print_number(number: i8) {
    println!("print function scope: {}", number);
}

fn get_highest<'a>(first_number: &'a i8, second_number: &'a i8) -> &'a i8 {
    if first_number > second_number {
	return first_number
    } else {
	return second_number
    }
}

fn process_transfer(stock: impl CanTransfer) -> () {
    stock.print();
    stock.transfer_stock();
}

fn main() {
    // let string_literal = "hello world";
    // print(string_literal.to_string());
    let test_string = &"Hello, World!";
    print(test_string);

    let mut result = 1.0 + 2.2;
    result = result + 3.3;
    println!("{}", result);

    let array: [i32; 3] = [1, 2, 3];
    println!("array has {} elements", array.len());
    for i in array.iter() {
	println!("{}", i);
    }

    let mut str_vector: Vec<&str> = vec!["one", "two", "three"];
    println!("{}", str_vector.len());
    str_vector.push("four");
    for i in str_vector.iter() {
	println!("{}", i);
    }

    let mut map = HashMap::new();
    map.insert("one", Value::Str("1"));
    map.insert("two", Value::Int(2));

    for (_key, value)in &map {
	match value {
	    Value::Str(inside_value) => {
		println!("the following value is an str: {}", inside_value);
	    }
	    Value::Int(inside_value) => {
		println!("the following value is an int: {}", inside_value);
	    }
	}
    }

    // let outcome: Option<&Value> = map.get("test");
    // println!("outcome passed");
    // let another_outcome: &Value = map.get("test").unwrap();
    // println!("another_outcome passed");

    // let one: i8 = 10;
    // let two: i8 = one + 5;
    // println!("{}", one);
    // println!("{}", two);

    // let one: String = String::from("one");
    // let two: String = one.to_owned() + " two";
    // println!("{}", two);
    // println!("{}", one);

    // let one: String = String::from("one");
    // {
    // 	println!("{}", &one);
    // 	let two: String = String::from("two");
    // }
    // println!("{}", one);
    // println!("{}", two);

    // let mut one: i8 = 1;
    // print_number(one);
    // alter_number(&mut one);
    // println!("main scope: {}", one);

    // let one;
    // {
    // 	let two: i8 = 2;
    // 	one = &two;
    // }
    // println!("r: {}", one);

    // let one: i8 = 1;
    // {
    // 	let two: i8 = 2;
    // 	let outcome: &i8 = get_highest(&one, &two);
    // 	println!("{}", outcome);
	
    // }

    // let stock: Stock = Stock::new("MonolithAi", 95.0);
    // let stock_two: Stock = Stock::new("BUMPER (former known as ASF)", 120.0)
    // 	.with_take_profit(100.0)
    // 	.with_stop_loss(50.0);
    // let mut stock: Stock = Stock::new("MonolithAi", 95.0);
    // stock.update_price(128.4);
    // println!("here is the stock: {}", stock.current_price);

    // let stock: Stock = Stock::new("MonolithAi", 95.0);
    // stock.print();
    // stock.transfer_stock();

    // let one = Coordinate{x: 50, y: 50};
    // let two = Coordinate{x: 500, y: 500};
    // let three = Coordinate{x: 5.6, y: 5.6};

    let mut x = String::from("test");
    capitalize!(x);
    println!("{}", x);
    
}
