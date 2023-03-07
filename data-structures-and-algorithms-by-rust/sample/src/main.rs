use std::time;

fn main() {
    let mut fibonacci = sample::Fibonacci {
	memo: vec![None; 51],
    };
    
    let now = time::Instant::now();
    println!("{:?}", fibonacci.calc(50));
    println!("{:?}",now.elapsed());
}

