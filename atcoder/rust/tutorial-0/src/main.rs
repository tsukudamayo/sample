use std::io::{stdin, Read};
use std::str::FromStr;

fn read<T: FromStr>() -> T {
    let stdin = stdin();
    let stdin = stdin.lock();
    let token: String = stdin.bytes()
        .map(|c| c.expect("failed to read char") as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect();
    token.parse().ok().expect("failed to parse")
}

fn answer_1(q1_1: u32, q1_2: u32) -> String {
    let answer = if (q1_1 * q1_2 % 2) == 0 { "Even" } else { "Odds" };
    return answer.to_string();
}

fn answer_2(q2: String) -> usize {
    return q2.chars().filter(|&c| c == '1').count();
}

fn answer_3(q_3: u32) -> u32 {
    let numbers = (0..q_3).map(|_| read::<u32>());
    let count_zero = numbers.map(|n| n.trailing_zeros());
    return count_zero.min().unwrap();
}

fn answer_4(a: u32, b: u32, c: u32, x: u32) -> u32 {
    let mut count: u32 = 0;
    for i in 0..a+1 {
	for j in 0..b+1 {
	    for k in 0..c+1 {
		if 500*i + 100*j + 50*k == x {
		    count += 1;
		}
	    }
	}
    }
    return count;
}

fn find_sum_of_digits(mut n: u32) -> u32 {
    let mut sum: u32 = 0;
    while  n > 0 {
	sum += n % 10;
	n /= 10;
    }
    return sum;
}

fn answer_5(n: u32, a: u32, b:u32) -> u32 {
    let mut total: u32 = 0;
    for i in 0..n+1 {
	let sum = find_sum_of_digits(i);
	if a <= sum && sum <= b {
	    total += i;
	}
    }
    return total;
}

fn answer_6(n: u32) -> u32 {
    let mut alice: u32 = 0;
    let mut bob: u32 = 0;
    let mut cards: Vec<u32> = (0..n).map(|_| read()).collect();
    cards.sort_by(|x, y| x.cmp(y).reverse());
    for (i, &x) in cards.iter().enumerate() {
	if i % 2 == 0 {
	    alice += x;
	} else {
	    bob += x;
	}
    }
    return alice - bob;
}

fn answer_7(n: u32) -> usize {
    let mut numbers: Vec<u32> = (0..n).map(|_| read()).collect();
    numbers.sort();
    numbers.dedup();
    return numbers.len();
}

fn main() {
    // // q1
    // let q1_1: u32 = read();
    // let q1_2: u32 = read();
    // let answer = answer_1(q1_1, q1_2);
    // println!("{}", answer);

    // // q2
    // let q2: String = read();
    // let answer = answer_2(q2);
    // println!("{}", answer);

    // // q3
    // let q_3: u32 = read();
    // let answer = answer_3(q_3);
    // println!("{}", answer);

    // // q4
    // let q_4_a = read();
    // let q_4_b = read();
    // let q_4_c = read();
    // let q_4_x = read();
    // let answer = answer_4(q_4_a, q_4_b, q_4_c, q_4_x);
    // println!("{}", answer);

    // // q5
    // let q5_n = read();
    // let q5_a = read();
    // let q5_b = read();
    // println!("{}", answer_5(q5_n, q5_a, q5_b));

    // // q6
    // let q6_n = read();
    // println!("{}", answer_6(q6_n));

    // q7
    let q7_n = read();
    println!("{}", answer_7(q7_n));
    
}
