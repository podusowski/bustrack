use std::collections::HashMap;
use std::io::{self, BufRead};
use std::iter::Iterator;

#[macro_use]
extern crate maplit;

mod ecsv;
use ecsv::Ecsv;

#[derive(Debug)]
struct Record {
    line: u32,
    lat: f32,
    lon: f32,
}

#[derive(Debug)]
struct RecordParseError;

impl From<std::num::ParseIntError> for RecordParseError {
    fn from(_: std::num::ParseIntError) -> RecordParseError {
        RecordParseError {}
    }
}

impl Record {
    fn from_map(map: HashMap<String, String>) -> Result<Record, RecordParseError> {
        Ok(Record {
            line: map["line"].parse::<u32>()?,
            lat: 0.0,
            lon: 0.0,
        })
    }
}

fn main() -> io::Result<()> {
    let input = io::stdin();
    let lines = input.lock().lines().filter_map(Result::ok);

    for elem in Ecsv::new(lines) {
        let elem = Record::from_map(elem);
        println!("{:?}", elem);
    }

    Ok(())
}
