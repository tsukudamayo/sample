use std::io::*;
use std::str::FromStr;

fn read<T: FromStr>() -> T {
    let stdin = stdin();
    let stdin = stdin.lock();
    let token: String = stdin
        .bytes()
        .map(|c| c.expect("failed to read char") as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect();
    token.parse().ok().expect("failed to parse token")
}

fn main() {
    // PracticeA - Welcome to AtCoder
    let a: u32 = read();
    let b: u32 = read();
    let c: u32 = read();
    let s: String = read();
    let sum: u32 = a + b + c;
    let sum_string: String = sum.to_string();
    println!("{} {}", sum_string, s);

    // ABC086A - Product
    let a: u32 = read();
    let b: u32 = read();
    let ans = if (a * b) % 2 == 0 { "Even" } else { "Odd" };
    println!("{}", ans);

    // ABC081A - Placing Marbles
    let mut count: i32 = 0;
    let inputs: String = read();
    let inputs_iter: Vec<char> = inputs.chars().collect();
    for i in inputs_iter.iter() {
	let tmp_string = i.to_string();
	if tmp_string == "1" {
	    count = count + 1;
	}
    }
    println!("{}", count);

    // // ABC081B - Shift only
    // let mut count: u32 = 0;
    // let num_of_inputs: u32 = read();
    // let inputs: String = read();
    // let inputs_iter: Vec<char> = inputs.chars().collect();
    // for i in inputs_iter.iter() {
    // 	let tmp_string: String = i.to_string();
    // 	let tmp_number: i32 = tmp_string.parse().unwrap();
    // 	if tmp_number % 2 != 0 {
    // 	    break
    // 	}
    // 	count = count + 1;
    // }
    // println!("{}", count);
}





