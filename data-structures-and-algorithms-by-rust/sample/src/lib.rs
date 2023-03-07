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

pub struct SSP {
    pub subset: Vec<i64>,
}

impl SSP {
    pub fn calc(&mut self, _d: usize, _t: i64) -> bool {
	match _d {
	    0 => {
		match _t {
		    0 => true,
		    _ => false,
		}
	    },
	    _ => {
		match self.calc(_d - 1, _t) {
		    true => true,
		    false => self.calc(_d - 1, _t - self.subset[_d - 1]),
		}
	    },
	}
    }
}


#[cfg(test)]
mod tests {
    use std::time;

    use crate::{Fibonacci, SSP};

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

    #[test]
    fn test_calc_ssp() {
	let _subset = vec![3, 2, 6, 5];
	let _target = 14;
	let _depth = _subset.len();
	let mut subset_sum_problem = SSP {
	    subset: _subset,
	};
	let res = subset_sum_problem.calc(_depth, _target);
	assert_eq!(res, true);
    }
}
