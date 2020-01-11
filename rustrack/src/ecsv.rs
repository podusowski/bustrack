use std::iter::Iterator;
use std::collections::HashMap;

struct Ecsv<T> where T: IntoIterator
{
    input: T::IntoIter,
    fmt: Vec::<String>
}

impl<'a, T> Ecsv<T> where T: IntoIterator<Item=&'a str>
{
    fn new(reader: T) -> Ecsv<T>
    {
        Ecsv::<T>{input: reader.into_iter(), fmt: Vec::new()}
    }
}

impl<'a, T> Iterator for Ecsv<T> where T: IntoIterator<Item=&'a str>
{
    type Item = HashMap::<String, String>;

    fn next(self: &mut Self) -> Option<Self::Item>
    {
        let mut ret = HashMap::<String, String>::new();

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
                    let items = self.fmt.iter().zip(items);
                    for (k, v) in items
                    {
                        // TODO: how to do this without string deep-copy?
                        ret.insert(k.to_string(), v.to_string());
                    }
                    return Some(ret);
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
        let input = vec!["$x;y", "1;2", "3;4", "$ lat;lon", "5;6"];
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
