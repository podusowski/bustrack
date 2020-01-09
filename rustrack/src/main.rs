use std::io::{self, Read};
use std::collections::HashMap;
use std::iter::Iterator;

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

struct Ecsv<Input> where Input: Iterator
{
    input: Input,
    fmt: Vec::<String>
}

impl<T> Ecsv<T> where T: Iterator
{
    fn new(reader: T) -> Ecsv<T>
    {
        Ecsv::<T>{input: reader, fmt: Vec::new()}
    }
}

impl<T> Iterator for Ecsv<T> where T: Iterator
{
    type Item = (String, String);

    fn next(self: &mut Self) -> Option<(String, String)>
    {
        None
    }
}

#[cfg(test)]
mod tests
{
    #[test]
    fn name() {
        let input = vec!["$x;y", "1,2", "3,4"];
        let ecsv = Ecsv::<Vec>::new(input);
    }
}

// TODO: implement this as an Iterator
fn read_ecsv(input: &mut std::io::BufRead) -> HashMap::<String, String>
{
    let mut buf = String::new();
    let mut fmt = Vec::<String>::new();
    let mut ret = HashMap::<String, String>::new();

    loop
    {
        let r = input.read_line(&mut buf);
        match r
        {
            Ok(0) => break,
            Err(_) => break,
            _ => ()
        }

        if buf.starts_with("#")
        {
            continue
        }
        else if buf.starts_with("$")
        {
            fmt = buf.trim().split(";").map(|s| s.to_string()).collect();
        }
        else
        {
            let items = buf.split(";");
            let items = fmt.iter().zip(items);
            for (k, v) in items
            {
                // TODO: how to do this without string deep-copy?
                ret.insert(k.to_string(), v.to_string());
            }
        }
    }

    ret
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
