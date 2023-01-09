use std::{str::FromStr, io::{stdin, Read}};

fn read<T: FromStr>() -> T {
    let stdin = stdin();
    let stdin = stdin.lock();
    let token: String = stdin.bytes()
        .map(|c| c.expect("failed map") as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect();
    token.parse().ok().expect("failed parse")
}

fn A() -> u32 {
    let A: u32 = read();
    let B: u32 = read();
    A.pow(B)
}

fn main() {
    println!("{}", A());
}
