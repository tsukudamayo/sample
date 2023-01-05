use crate::util;

pub fn answer() -> u32 {
    let A: u32 = util::read();
    let B: u32 = util::read();
    return A.pow(B);
}
