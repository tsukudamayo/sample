pub struct Fibonacci {
    pub memo: Vec<Option<usize>>,
}

impl Fibonacci {
    pub fn calc(&mut self, number: usize) -> usize {
	self.memo[number].unwrap_or_else(|| self.fib(number))
    }

    fn fib(&mut self, number: usize) -> usize {
	match number {
	    0 => 0,
	    1 => 1,
	    n => {
		let calc = self.calc(n - 1) + self.calc(n - 2);
		self.memo[number] = Some(calc);
		calc
	    },
	}		
    }
}

#[cfg(test)]
mod tests {
    use std::time;

    use crate::Fibonacci;

    #[test]
    fn test_calc_fibonacci() {
	let mut fibonacci = Fibonacci {
	    memo: vec![None; 51],
	};

	let res = fibonacci.calc(0);
	assert_eq!(res, 0);

	let res = fibonacci.calc(1);
	assert_eq!(res, 1);

	let res = fibonacci.calc(2);
	assert_eq!(res, 1);

	let res = fibonacci.calc(3);
	assert_eq!(res, 2);

	let res = fibonacci.calc(8);
	assert_eq!(res, 21);

	let now = time::Instant::now();
	let res = fibonacci.calc(50);
	println!("{:?}",now.elapsed());
	assert_eq!(res, 12586269025);
    }
}
