use std::io;
use std::iter::Iterator;

#[macro_use] extern crate maplit;

mod ecsv;

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
