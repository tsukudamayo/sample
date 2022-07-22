use std::collections::HashMap;

enum Value {
    Str(&'static str),
    Int(i32),
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

fn check_int_above_threshold(
    threshold: i32,
    get_retuslt: Option<&Value>
) -> Result<bool, &'static str> {
    match get_retuslt {
	Some(inside_value) => {
	    match inside_value {
		Value::Str(_) => return Err(
		    "str value was supplied as opposed to an int which is needed"
		),
		Value::Int(int_value) => {
		    if int_value > &threshold {
			return Ok(true)
		    }
		    return Ok(false)
		}
	    }
	}
	None => return Err("no value was supplied to be checked")
    }
}

fn main() {
    let test_string = &"Hello, World";
    print(test_string);

    let array: [i32; 3] = [1, 2, 3];
    println!("array has {} elements", array.len());

    for i in array.iter() {
	println!("{}", i);
    }

    let array: [i32; 3] = [1, 2, 3];
    println!("array has {} elements", array.len());

    let mut str_vector: Vec<&str> = vec!["one", "two", "three"];
    println!("{}", str_vector.len());
    str_vector.push("four");
    for i in str_vector.iter() {
	println!("{}", i);
    }

    let mut map = HashMap::new();
    map.insert("one", Value::Str("1"));
    map.insert("two", Value::Int(2));

    for (_key, value) in &map {
	match value {
	    Value::Str(inside_value) => {
		println!("the following value is an str: {}", inside_value);
	    }
	    Value::Int(inside_value) => {
		println!("the following value is an int: {}", inside_value);
	    }
	}
    }
    match map.get("test") {
	Some(inside_value) => {
	    process_enum(inside_value);
	}
	None => {
	    println!("there is no value");
	}
    }
}
