use std::{str::FromStr, io::{stdin, Read}};

fn read<T: FromStr>() -> T {
    let stdin = stdin();
    let stdin = stdin.lock();
    let token: String = stdin.bytes()
        .map(|c| c.expect("map failed") as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect();
    token.parse().ok().expect("parse failed")
}

fn b() -> Vec<Vec<u32>> {
    println!("{}", "Enter N");
    let n: u32 = read();
    println!("{}", "Enter A1...An");
    let a: Vec<u32> = (0..n).map(|_| read()).collect();
    println!("{}", "Enter Q");
    let q: u32 = read();
    println!("{}", "Enter query");
    let mut all_query: Vec<Vec<u32>> = Vec::new();
    for i in 0..q {
	println!("query {}", "i");
	let query: Vec<u32> = (0..q).map(|_| read()).collect();
	all_query.push(query);
    }
    all_query
}

fn main() {
    for i in b().iter() {
	println!("{:?}", i);
    }
}
