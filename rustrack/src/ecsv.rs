use std::iter::{Iterator, FromIterator};
use std::collections::HashMap;

pub struct Ecsv<T> where T: IntoIterator
{
    input: T::IntoIter,
    fmt: Vec::<String>
}

impl<T> Ecsv<T> where T: IntoIterator<Item=String>
{
    pub fn new(reader: T) -> Ecsv<T>
    {
        Ecsv::<T>{input: reader.into_iter(), fmt: Vec::new()}
    }
}

impl<T> Iterator for Ecsv<T> where T: IntoIterator<Item=String>
{
    type Item = HashMap::<String, String>;

    fn next(self: &mut Self) -> Option<Self::Item>
    {
        loop
        {
            match self.input.next()
            {
                Some(s) if s.starts_with("#") => continue,
                Some(s) if s.starts_with("$") => {
                    self.fmt = s[1..].trim().split(";").map(|s| s.to_string()).collect();
                    continue
                },
                Some(s) => {
                    let items = s.split(";");
                    let items = self.fmt.iter().zip(items).map(|x| (x.0.to_string(), x.1.to_string()));
                    return Some(HashMap::from_iter(items));
                },
                None => return None,
            }
        }
    }
}

#[cfg(test)]
mod tests
{
    #[test]
    fn read_simple_ecsv() {
        let input = ["$x;y", "1;2", "3;4", "$ lat;lon", "5;6"].iter().map(|s| s.to_string());
        let mut ecsv = super::Ecsv::new(input);

        assert_eq!(Some(hashmap!("x".to_string() => String::from("1"),
                                 String::from("y") => String::from("2"))), ecsv.next());

        assert_eq!(Some(hashmap!(String::from("x") => String::from("3"),
                                 String::from("y") => String::from("4"))), ecsv.next());

        assert_eq!(Some(hashmap!(String::from("lat") => String::from("5"),
                                 String::from("lon") => String::from("6"))), ecsv.next());

        assert_eq!(None, ecsv.next());
    }
}
