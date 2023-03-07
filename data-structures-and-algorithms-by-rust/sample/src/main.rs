use sample::SSP;

fn main() {
    let _subset = vec![3, 2, 6, 5];
    let _target = 14;
    let _depth = _subset.len();
    let mut subset_sum_problem = SSP {
	subset: _subset,
    };

    println!("{}", subset_sum_problem.calc(_depth, _target));
    
}

