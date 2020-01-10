use std::io::{self, Read};
use std::collections::HashMap;
use std::iter::Iterator;

#[macro_use] extern crate maplit;

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

struct Ecsv<Input> where Input: Iterator<Item=String>
{
    input: Input,
    fmt: Vec::<String>
}

impl<T> Ecsv<T> where T: Iterator<Item=String>
{
    fn new(reader: T) -> Ecsv<T>
    {
        Ecsv::<T>{input: reader, fmt: Vec::new()}
    }
}

impl<T> Iterator for Ecsv<T> where T: Iterator<Item=String>
{
    type Item = HashMap::<String, String>;

    fn next(self: &mut Self) -> Option<Self::Item>
    {
        let mut buf = String::new();
        let mut ret = HashMap::<String, String>::new();

        loop
        {
            let r = self.input.next();

            match r
            {
                Some(s) if s.starts_with("#") => continue,
                Some(s) if s.starts_with("$") => {
                    self.fmt = buf.trim().split(";").map(|s| s.to_string()).collect();
                    continue
                },
                Some(s) => {
                    let items = s.split(";");
                    let items = self.fmt.iter().zip(items);
                    for (k, v) in items
                    {
                        // TODO: how to do this without string deep-copy?
                        ret.insert(k.to_string(), v.to_string());
                    }
                    return Some(ret);
                },
                None => (),
            }
        }
    }
}

#[cfg(test)]
mod tests
{
    #[test]
    fn name() {
        let input = [String::from("$x;y"), String::from("1,2"), String::from("3,4")];
        let mut ecsv = super::Ecsv::new(input.iter());
        assert_eq!(Some(hashmap!(String::from("1") => String::from("2"))), ecsv.next());
    }
}

fn main() -> io::Result<()>
{
    let mut buf = String::new();
    let mut fmt = Vec::<String>::new();

    loop
    {
        io::stdin().read_line(&mut buf)?;
        if buf.starts_with("#")
        {
            continue
        }
        else if buf.starts_with("$")
        {
            fmt = buf.trim().split(";").map(|s| s.to_string()).collect();
        }

        let r = Record::from_string(&buf);
        println!("Hello, world! {}", buf);
        println!("fmt: {:?}", fmt);
    }

    Ok(())
}
