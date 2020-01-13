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
struct RecordParseError {
    what: String
}

impl From<std::num::ParseIntError> for RecordParseError {
    fn from(_: std::num::ParseIntError) -> RecordParseError {
        RecordParseError {}
    }
}

impl From<std::num::ParseFloatError> for RecordParseError {
    fn from(_: std::num::ParseFloatError) -> RecordParseError {
        RecordParseError {}
    }
}

fn get_parsed<T: std::str::FromStr>(map: &HashMap<String, String>, key: &str) -> Result<T, ()> {
    if let Some(value) = map.get(key) {
        match value.parse::<T>() {
            Ok(value) => return Ok(value),
            Err(error) => return Err(error.to_string())
        }
    }
    Err(())
}

impl Record {
    fn from_map(map: HashMap<String, String>) -> Result<Record, ()> {
        Ok(Record {
            line: get_parsed(&map, "line")?,
            lat: get_parsed(&map, "lat")?,
            lon: get_parsed(&map, "lon")?
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
