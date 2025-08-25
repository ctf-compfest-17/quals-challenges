from io import StringIO

red_ns = []

def parse_rle(bitstring: str, read: int, buffer: StringIO):
    ori_read = read
    length = bitstring[read]
    while bitstring[read] != "0":
        read += 1
        length += bitstring[read]

    read += 1
    read_next_n_bit = len(length)
    value = bitstring[read:read + read_next_n_bit]
    length_s = length
    value_s = value

    read += read_next_n_bit
    length = int(length, 2)
    value = int(value, 2)
    n = length + value + 1
    # red_ns.append(n)
    # print(f"{ori_read = }, {n = }, {length_s = }, {value_s = }, {len(length_s) = }, {len(value_s) = }")

    for _ in range(n):
        buffer.write("00")

    return read


def parse_data(bitstring: str, read: int, buffer: StringIO, buffer_size: int) -> int:
    cur_pair = bitstring[read:read+2]
    while cur_pair != "00":
        # print(cur_pair)
        buffer.write(cur_pair)
        read += 2
        cur_pair = bitstring[read:read+2]

    # print(cur_pair)
    return read + 2


def delta_decode_plane(plane: str) -> str:
    output = StringIO()
    prev_bit = "0"
    for bit in plane:
        if bit == "0":
            output.write(prev_bit)
        else:
            prev_bit = "1" if prev_bit == "0" else "0"
            output.write(prev_bit)

    return output.getvalue()


def xor_planes(plane_a: list[int], plane_b: list[int]) -> list[int]:
    return [a ^ b for a, b in zip(plane_a, plane_b)]


with open("compressed_flag_mirror.dat", "rb") as f:
    comp = f.read()

bitstring = StringIO()
for b in comp:
    bitstring.write(bin(b)[2:].rjust(8, "0"))
del comp
bitstring = bitstring.getvalue()

width = int(bitstring[:7], 2)
height = int(bitstring[7:14], 2)
enc_mode = int(bitstring[14:16], 2)
print(f"{enc_mode = }")
rr = []

plane_size = width * 8 * height * 8 * 8 # in bits
read = 16
packet_type = int(bitstring[read])
read += 1
red_plane = StringIO()
while red_plane.tell() < plane_size:
    # print(packet_type, read)
    if packet_type == 0:
        read = parse_rle(bitstring, read, red_plane)
    else:
        rr.append(red_plane.tell())
        read = parse_data(bitstring, read, red_plane, plane_size)
    packet_type = 1 - packet_type
    # print(red_plane.tell())

print("red done")

gr = []
green_plane = StringIO()
packet_type = int(bitstring[read])
read += 1
while green_plane.tell() < plane_size:
    if packet_type == 0:
        read = parse_rle(bitstring, read, green_plane)
    else:
        gr.append(green_plane.tell())
        read = parse_data(bitstring, read, green_plane, plane_size)
    packet_type = 1 - packet_type

print("green done")

br = []
blue_plane = StringIO()
packet_type = int(bitstring[read])
read += 1
while blue_plane.tell() < plane_size:
    if packet_type == 0:
        read = parse_rle(bitstring, read, blue_plane)
    else:
        br.append(blue_plane.tell())
        read = parse_data(bitstring, read, blue_plane, plane_size)
    packet_type = 1 - packet_type

print("blue done")

red_plane = red_plane.getvalue()
green_plane = green_plane.getvalue()
blue_plane = blue_plane.getvalue()

assert len(red_plane) == plane_size, f"{len(red_plane) = }"
assert len(green_plane) == plane_size, f"{len(green_plane) = }"
#assert len(blue_plane) == plane_size, f"{len(blue_plane) = }"
blue_plane = blue_plane[:plane_size]

if enc_mode == 3:
    red_plane = delta_decode_plane(red_plane)
    green_plane = delta_decode_plane(green_plane)
    blue_plane = delta_decode_plane(blue_plane)
    
    red_plane = [int(red_plane[i:i+8], 2) for i in range(0, len(red_plane), 8)]
    green_plane = [int(green_plane[i:i+8], 2) for i in range(0, len(green_plane), 8)]
    blue_plane = [int(blue_plane[i:i+8], 2) for i in range(0, len(blue_plane), 8)]

    blue_plane = xor_planes(green_plane, blue_plane)
    green_plane = xor_planes(red_plane, green_plane)
    
elif enc_mode == 2:
    red_plane = delta_decode_plane(red_plane)

    red_plane = [int(red_plane[i:i+8], 2) for i in range(0, len(red_plane), 8)]
    green_plane = [int(green_plane[i:i+8], 2) for i in range(0, len(green_plane), 8)]
    blue_plane = [int(blue_plane[i:i+8], 2) for i in range(0, len(blue_plane), 8)]

    blue_plane = xor_planes(green_plane, blue_plane)
    green_plane = xor_planes(red_plane, green_plane)

else: # only other option is 1
    red_plane = delta_decode_plane(red_plane)
    green_plane = delta_decode_plane(green_plane)
    blue_plane = delta_decode_plane(blue_plane)

    red_plane = [int(red_plane[i:i+8], 2) for i in range(0, len(red_plane), 8)]
    green_plane = [int(green_plane[i:i+8], 2) for i in range(0, len(green_plane), 8)]
    blue_plane = [int(blue_plane[i:i+8], 2) for i in range(0, len(blue_plane), 8)]


from PIL import Image

pixel_array = []

for r, g, b in zip(red_plane, green_plane, blue_plane):
    pixel_array.append(r)
    pixel_array.append(g)
    pixel_array.append(b)

img = Image.frombytes("RGB", (width*8, height*8), bytes(pixel_array))
img.save("test_out_mirror.bmp", format="BMP")

# print(red_plane[:10])
