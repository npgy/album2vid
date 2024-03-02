use std::path::{Path};

use clap::{arg, command, ArgMatches, Error, error::ErrorKind};

fn check_dir(path: &str) -> Result<String, Error> {
    let is_dir = Path::new(path).is_dir();
    let err = Error::raw(ErrorKind::ValueValidation, "Not a valid directory!");
    
    match is_dir {
        true => Ok(path.to_owned()),
        false => Err(err)
    }
}

fn main() {
    let albist_cmd: ArgMatches = command!()
    .arg(
        arg!([path] "The full path to the album's folder")
        .required(true)
        .value_parser(clap::builder::ValueParser::new(check_dir))
    )
    .arg(
        arg!(-f --fast ... "Enables fast mode, may cause rendering errors")
    )
    .get_matches();

    if let Some(fast) = albist_cmd.get_one::<u8>("fast") {
        println!("{fast}");
    }
}
