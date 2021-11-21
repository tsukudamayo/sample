#[derive(Debug)]
struct Person {
    name: String,
    age: u32,
}

#[derive(Debug)]
enum Event {
    Quit,
    KeyDown(u8),
    MouseDown { x: i32, y: i32 },
}

fn main() {    
    let s1: String = String::from("Hello, World!");
    println!("{}", s1);
    let s2: &str = &s1;
    println!("{}", s2);
    let s3: String = s2.to_string();
    println!("{}", s3);

    let mut t = (1, "2");
    println!("{}", t.0);
    println!("{}", t.1);

    let mut a: [i32; 3] = [0, 1, 2];
    let b: [i32; 3] = [0; 3];
    a[1] = b[1];
    a[2] = b[2];
    println!("{:?}", &a[1..3]);

    let e1 = Event::Quit;
    let e2 = Event::MouseDown { x: 10, y: 10 };
    println!("{:?}", e1);
    println!("{:?}", e2);

    let result: Result<i32, String> = Ok(200);
    println!("code : {}", result.unwrap_or(-1));
    let result: Result<i32, String> = Err("error".to_string());
    println!("code : {}", result.unwrap_or(-1));
}
