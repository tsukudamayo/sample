mod stocks;
use stocks::{open_order, close_order};
use stocks::structs::order::Order;
use stocks::enums::order_types::OrderType;
use stocks::structs::stock::Stock;
use serde_json::{json, Value};

fn main() {
    // let stock: Value = json!({
    // 	"name": "MonolithAi",
    // 	"price": 43.7,
    // 	"history": [19.4, 26.9, 32.5],
    // });
    // println!("first price: {}", stock["history"][0]);
    // println!("{}", stock.to_string());

    let stock: Stock = Stock::new("MonolithAi", 36.5);
    println!("here is the stock name : {}", stock.name);
    println!("here is the stock name :{}", stock.current_price);

    println!("hello stocks");
    let mut new_order: Order = open_order(20, OrderType::Long, "bumper", 56.8, None, None);
    println!("the current price is: {}", &new_order.current_value());
    println!("the current profit is: {}", &new_order.current_profit());

    new_order.stock.update_price(43.1);
    println!("the current price is: {}", &new_order.current_value());
    println!("the current profit is: {}", &new_order.current_profit());
    new_order.stock.update_price(82.7);
    println!("the current price is : {}", &new_order.current_value());
    println!("the current profit is: {}", &new_order.current_profit());

    let profit: f32 = close_order(new_order);
    println!("we made {} profit", profit);
}
