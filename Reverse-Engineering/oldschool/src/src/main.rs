use std::env;
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};
use std::path::Path;

fn check_validity(width: u32, height: u32, bpp: u16) -> bool {
    if height > (i32::MAX as u32) {
        println!("Height can't be negative!");
        return false;
    }

    if width != height {
        println!("Width and height can't have different dimensions");
        return false;
    }

    if (width % 8 != 0) || (height % 8 != 0) {
        println!("Width and height must be a multiply of 8");
        return false;
    }

    if ((width / 8) > 127) || ((height / 8) > 127) {
        println!("Asset can't have more than 127 tiles");
        return false;
    }

    if bpp != 24 {
        println!("Color depth needs to be 24-bit");
        return false;
    }

    return true;
}

fn delta_encode_plane(plane: &[u8]) -> Vec<u8> {
    let mut prev_bit = 0u8;
    let mut current_byte = 0u8;

    let mut output = Vec::with_capacity(plane.len());
    for &byte in plane {
        for current_bit_pos in (0..7u8).rev() {
            let current_bit = byte & (1 << current_bit_pos);
            current_byte |= (prev_bit ^ current_bit) << current_bit_pos;
            prev_bit = current_bit;
        }
        output.push(current_byte);
        current_byte = 0;
    }

    output
}

fn xor_planes(plane_a: &[u8], plane_b: &[u8]) -> Vec<u8> {
    let mut output = Vec::with_capacity(plane_a.len());
    for (a, b) in plane_a.iter().zip(plane_b) {
        output.push(a ^ b);
    }

    output
}

fn enc_mode1(rplane: &[u8], gplane: &[u8], bplane: &[u8]) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let rplane = delta_encode_plane(rplane);
    let gplane = delta_encode_plane(gplane);
    let bplane = delta_encode_plane(bplane);
    
    (rplane, gplane, bplane)
}

fn enc_mode2(rplane: &[u8], gplane: &[u8], bplane: &[u8]) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let gplane = xor_planes(&rplane, &gplane);
    let bplane = xor_planes(&gplane, &bplane);
    let rplane = delta_encode_plane(rplane);
    
    (rplane, gplane, bplane)
}

fn enc_mode3(rplane: &[u8], gplane: &[u8], bplane: &[u8]) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let gplane = xor_planes(&rplane, &gplane);
    let bplane = xor_planes(&gplane, &bplane);
    let rplane = delta_encode_plane(rplane);
    let gplane = delta_encode_plane(&gplane);
    let bplane = delta_encode_plane(&bplane);
    
    (rplane, gplane, bplane)
}

fn compress_plane(plane: &mut [u8]) -> (Vec<u8>, u8) {
    let mut output = Vec::<u8>::new();
    let initial_type = plane[0] & 0xC0; // 00 -> type 0/RLE, anything else -> type 1/Data
    let initial_packet = if initial_type == 0 {0u8} else {1u8 << 7};
    output.push(initial_packet);
    let mut last_idx = output.len() - 1;
    let mut placed_bits = 1u8;
    let mut i = 0usize;
    let mut processed = 0u8; // amount of bits that have been processed in the current byte
    while i < plane.len() {
        // let mut tmp_arr = Vec::<u8>::new();
        let mut cur_buffer = output[last_idx];
        let mut cnt = 0u32;
        'rle: while i < plane.len() { // RLE Packet loop
            if (i == 0) && (initial_type != 0) { // If initial type is Data then don't do this loop
                break;
            }
            // println!("Progress: {i}/{}", plane.len());
            let mut byte = plane[i];
            for _ in 0..4 {
                if (byte & 0xC0) == 0 {
                    cnt += 1;
                    processed += 2;
                    byte <<= 2;
                } else {
                    plane[i] = byte;
                    cnt += 1;
                    let mask = 1u32 << (32 - cnt.leading_zeros() - 1);
                    let val = cnt ^ mask;
                    let len = mask - 2;

                    let n_bytes = [
                        (len >> 24) as u8, (len >> 16) as u8, (len >> 8) as u8, (len & 0xFF) as u8,
                        (val >> 24) as u8, (val >> 16) as u8, (val >> 8) as u8, (val & 0xFF) as u8,
                    ];

                    // bit manip stuff
                    // println!("val = {val}, len = {len}, mask = {mask:032b}");
                    // std::process::exit(0);
                    cur_buffer |= n_bytes[0] >> placed_bits;
                    output[last_idx] = cur_buffer;
                    let inserted_bits = 8 - placed_bits;
                    for idx in 0..(n_bytes.len()-1) {
                        cur_buffer = (n_bytes[idx] << inserted_bits) | (n_bytes[idx+1] >> placed_bits);
                        output.push(cur_buffer);
                        last_idx += 1;
                    }
                    cur_buffer = n_bytes[7] << inserted_bits;
                    output.push(cur_buffer);
                    last_idx += 1;
                    placed_bits = inserted_bits;
                    break 'rle;
                }
            }
            i += 1;
            processed = 0;
        }
                    
        let mut cur_buffer = output[last_idx];
        'data: while i < plane.len() { // Data Packet loop
            // println!("Progress: {i}/{}", plane.len());
            let mut byte = plane[i];
            let mut last_bit = byte & 0x80;
            byte <<= 1;
            processed += 1;
            while processed < 8 {
                let cur_bit = byte & 0x80;
                if (last_bit == 0) && (cur_bit == 0) {
                    byte >>= 1;
                    plane[i] = byte;
                    processed -= 1;
                    match placed_bits {
                        0..6 => {
                            output.push(cur_buffer);
                            last_idx += 1;
                            placed_bits += 2;
                        }
                        6 => {
                            output.push(cur_buffer);
                            output.push(0);
                            placed_bits = 0;
                            last_idx += 2;
                        }
                        7 => {
                            output.push(cur_buffer);
                            output.push(0);
                            placed_bits = 1;
                            last_idx += 2
                        }
                        _ => unreachable!()
                    }
                    break 'data;
                } else {
                    byte <<= 1;
                    processed += 1;
                    match placed_bits {
                        0..6 => {
                            cur_buffer |= last_bit >> placed_bits;
                            cur_buffer |= cur_bit >> (placed_bits + 1);
                            placed_bits += 2;
                        },
                        6 => {
                            cur_buffer |= last_bit >> placed_bits;
                            cur_buffer |= cur_bit >> (placed_bits + 1);
                            output.push(cur_buffer);
                            cur_buffer = 0;
                            placed_bits = 0;
                            last_idx += 1;
                        },
                        7 => {
                            cur_buffer |= last_bit >> placed_bits;
                            output.push(cur_buffer);
                            cur_buffer = cur_bit;
                            placed_bits = 1;
                            last_idx += 1;
                        },
                        _ => unreachable!()
                    }
                    last_bit = byte & 0x80;
                    processed += 1;
                }
            }
            i += 1;
            processed = 0;
        }
    }

    (output, placed_bits)
}

fn pack_planes(plane_a: &[u8], last_pos_a: u8, plane_b: &[u8], last_pos_b: u8) -> (Vec<u8>, u8) {
    let mut output = Vec::with_capacity(plane_a.len() + plane_b.len());
    let mut pos;

    for &byte in plane_a {
        output.push(byte);
    }

    if last_pos_a == 0 {
        for &byte in plane_b {
            output.push(byte);
        }
        pos = last_pos_b;
    } else {
        let mut last_idx = output.len() - 1;
        let mut last_byte = output[last_idx];
        pos = last_pos_a;
        for &byte in plane_b {
            last_byte |= byte >> pos;
            output[last_idx] = last_byte;
            let inserted = 8 - pos;
            last_byte = byte << inserted;
            output.push(last_byte);
            pos = inserted;
            last_idx += 1;
        }
    }

    (output, pos)
}

fn pack(header: u16, red: &[u8], red_pos: u8, green: &[u8], green_pos: u8, blue: &[u8], blue_pos: u8) -> Vec<u8> {
    let (red_green, red_green_pos) = pack_planes(red, red_pos, green, green_pos);
    let (red_green_blue, _) = pack_planes(&red_green, red_green_pos, blue, blue_pos); 
    
    let tmp = [(header >> 8) as u8, (header & 0xFF) as u8];
    let output = [tmp.as_slice(), red_green_blue.as_slice()].concat();

    output
}

fn compress(data: Vec<u8>) -> Vec<u8> {
    let arr_offset = u32::from_le_bytes([data[0x0a], data[0x0b], data[0x0c], data[0x0d]]) as usize;
    let width = u32::from_le_bytes([data[0x12], data[0x13], data[0x14], data[0x15]]);
    let height = u32::from_le_bytes([data[0x16], data[0x17], data[0x18], data[0x19]]);
    let bpp = u16::from_le_bytes([data[0x1c], data[0x1d]]);

    if !check_validity(width, height, bpp) {
        std::process::exit(1);
    }

    let wtiles = (width / 8) as u8;
    let htiles = (height / 8) as u8;
    
    let row_size = ((bpp as u32)*width+31)/32 * 4;
    let pixel_array_size = (row_size * height) as usize;

    let plane_size = (width as usize) * (height as usize);
    let mut red_plane = Vec::with_capacity(plane_size);
    let mut green_plane = Vec::with_capacity(plane_size);
    let mut blue_plane = Vec::with_capacity(plane_size);

    for chunk in data[arr_offset..(pixel_array_size+arr_offset)].chunks_exact(3) {
        let (r, g, b) = (chunk[0], chunk[1], chunk[2]);
        red_plane.push(r);
        green_plane.push(g);
        blue_plane.push(b);
    }

    let time = match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(n) => n.as_secs(),
        Err(_) => {
            println!("Error getting current time since EPOCH");
            std::process::exit(1);
        }
    };

    let enc_mode = (time % 3) + 1;
    match enc_mode {
        1 => {
            (red_plane, green_plane, blue_plane) = enc_mode1(&red_plane, &green_plane, &blue_plane);
        },
        2 => {
            (red_plane, green_plane, blue_plane) = enc_mode2(&red_plane, &green_plane, &blue_plane);
        },
        3 => {
            (red_plane, green_plane, blue_plane) = enc_mode3(&red_plane, &green_plane, &blue_plane);
        },
        _ => unreachable!()
    }

    let packed_header = ((wtiles as u16) << 9) | ((htiles as u16) << 2) | (enc_mode as u16);
    let (comp_red, last_pos_red) = compress_plane(&mut red_plane);
    let (comp_green, last_pos_green) = compress_plane(&mut green_plane);
    let (comp_blue, last_pos_blue) = compress_plane(&mut blue_plane);
    
    pack(packed_header, &comp_red, last_pos_red, &comp_green, last_pos_green, &comp_blue, last_pos_blue)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: oldschool.exe <BMP file path>");
        std::process::exit(1);
    }

    let file_path = Path::new(&args[1]);
    let data = match fs::read(file_path) {
        Ok(res) => res,
        Err(_) => {
            println!("Error reading file: {}", file_path.to_str().unwrap());
            std::process::exit(1);
        }
    };
    let output = compress(data);
    let filename: Vec<&str> = file_path.file_name().unwrap().to_str().unwrap().split(".").collect();
    let out_filename = format!("compressed_{}.dat", filename[0]);
    match fs::write(&out_filename, &output) {
        Ok(_) => println!("File compressed successfully!"),
        Err(_) => {
            println!("Error writing file: {}", &out_filename);
            std::process::exit(1);
        }
    }
}
