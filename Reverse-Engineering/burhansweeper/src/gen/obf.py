from hashlib import sha256
from random import randint, seed

seed('asoidigjwp9egjawg')

def gen_coords():
    res = set()
    while len(res) < 300:  # generate more to ensure uniqueness filtering works
        x = randint(1, 32)
        y = randint(1, 32)
        z = randint(1, 32)
        res.add((x, y, z))
    return list(res)

def hash16(val: int) -> str:
    return sha256(str(val & 0xFFFFFFFF).encode()).hexdigest()[:16]

def eq1(x, y, z): return ((x * 73856093) ^ (y * 19349663) ^ (z * 83492791)) & 0xFFFFFFFF
def eq2(x, y, z): return ((x << 11) | (y << 5) | (z << 3)) ^ (x * y * z) & 0xFFFFFFFF
def eq3(x, y, z): return ((x ^ (z << 7)) + (y ^ (x << 3)) - (z ^ (y << 1))) & 0xFFFFFFFF

coords = gen_coords()
hashes = set()
valid = []

for x, y, z in coords:
    h1 = hash16(eq1(x, y, z))
    h2 = hash16(eq2(x, y, z))
    h3 = hash16(eq3(x, y, z))
    key = (h1, h2, h3)
    if key in hashes:
        continue
    hashes.add(key)
    valid.append((x, y, z))
    if len(valid) >= 170:
        break

t1 = ','.join(f'"{hash16(eq1(x, y, z))}"' for x, y, z in valid)
t2 = ','.join(f'"{hash16(eq2(x, y, z))}"' for x, y, z in valid)
t3 = ','.join(f'"{hash16(eq3(x, y, z))}"' for x, y, z in valid)

lua_code = f'''

function Cell.isSafe(self)
    local bit32 = require("lib.bit32")
    local x = self.x
    local y = self.y
    local z = self.z

    local t1 = {{{t1}}}
    local t2 = {{{t2}}}
    local t3 = {{{t3}}}

    local function hash16(v)
        return string.sub(love.data.encode("string", "hex", love.data.hash("sha256", tostring(v % 4294967296))), 1, 16)
    end

    local a1 = hash16(bit32.bxor(x * 73856093, bit32.bxor(y * 19349663, z * 83492791)))
    local a2 = hash16(bit32.bxor(bit32.bor(bit32.lshift(x, 11), bit32.bor(bit32.lshift(y, 5), bit32.lshift(z, 3))), x * y * z))
    local a3 = hash16((bit32.bxor(x, bit32.lshift(z, 7)) + bit32.bxor(y, bit32.lshift(x, 3)) - bit32.bxor(z, bit32.lshift(y, 1))) % 4294967296)

    local check1, check2, check3 = false, false, false

    for _, v in ipairs(t1) do if v == a1 then check1 = true break end end
    for _, v in ipairs(t2) do if v == a2 then check2 = true break end end
    for _, v in ipairs(t3) do if v == a3 then check3 = true break end end

    return check1 and check2 and check3
end

'''

with open('./out.txt', 'w') as f:
    f.write(lua_code)

with open('./coords.txt', 'w') as f:

    f.write('{')
    for x, y, z in valid:
        f.write(f'{{{x},{y},{z}}},')
    f.write('}')