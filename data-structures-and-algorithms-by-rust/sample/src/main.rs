use std::rc::Rc;

use sample::Frog;

fn main() {
    let _hights = vec![2, 9, 4, 5, 1, 6, 10];
    let length = _hights.len();
    let mut frog = Rc::new(Frog {
	costs: vec![0; length],
	hights: _hights,
    });

    frog.calc();
    println!("{:#?}", frog.costs);
}

