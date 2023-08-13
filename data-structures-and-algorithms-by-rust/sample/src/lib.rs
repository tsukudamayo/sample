use std::rc::Rc;

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

// #[derive(Debug)]
// pub struct Frog {
//     pub hights:  Vec<i64>,
//     pub costs: Vec<i64>,
// }

// impl Frog {
//     pub fn calc(&mut self) {
// 	for (idx, _) in self.hights.iter().enumerate() {
// 	    match idx {
// 		0 => self.costs[0] = 0,
// 		1 => {
// 		    let prev = (self.hights[1] - self.hights[0]).abs();
// 		    self.chmin(1, &prev)
// 		},
// 		i => {
// 		    let prev_1 = (self.hights[i] - self.hights[i - 1]).abs() + self.costs[i - 1];
// 		    let prev_2 = (self.hights[i] - self.hights[i - 2]).abs() + self.costs[i - 2];
// 		    self.chmin(i, &prev_1);
// 		    self.chmin(i, &prev_2)
// 		},
// 	    }
// 	}
//     }

//     fn chmin(&mut self, idx: usize, b: &i64 ) {
// 	if self.costs[idx] > *b {
// 	    self.costs[idx] = *b
// 	}
//     }
// }

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
