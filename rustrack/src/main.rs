use std::io::{self, BufRead};
use std::iter::Iterator;

#[macro_use] extern crate maplit;

mod ecsv;
use ecsv::Ecsv;

struct Record
{
    line: u32,
    lat: f32,
    lon: f32
}

impl Record
{
    fn from_string(s: &str) -> Record
    {
        Record{line: 0, lat: 0.0, lon: 0.0}
    }
}

fn main() -> io::Result<()>
{
    let input = io::stdin();
    let lines = input.lock().lines().filter_map(Result::ok);

    for elem in Ecsv::new(lines) {
        println!("{:?}", elem);
    }

    Ok(())
}
