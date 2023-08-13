use std::rc::Rc;

use sample::SSP;
// use sample::Frog;

fn main() {
    let _subset = vec![3, 2, 6, 5];
    let _target = 14;
    let _depth = _subset.len();
    let mut subset_sum_problem = SSP {
	subset: _subset,
    };
    println!("{}", subset_sum_problem.calc(_depth, _target));
    
    // let _hights = vec![2, 9, 4, 5, 1, 6, 10];
    // let length = _hights.len();
    // let mut frog = Rc::new(Frog {
    // 	costs: vec![0; length],
    // 	hights: _hights,
    // });

    // frog.calc();
    // println!("{:#?}", frog.costs);
}

