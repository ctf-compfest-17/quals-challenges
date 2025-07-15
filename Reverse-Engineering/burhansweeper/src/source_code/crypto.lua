local crypto = {}
local bit32 = require("lib.bit32")


local function hexToBytes(hex)
    return love.data.decode("string", "base64", hex)
end

local function xor(data, key)
    local result = {}
    for i = 1, #data do
        local k = key:byte((i - 1) % #key + 1)
        local d = data:byte(i)
        table.insert(result, string.char(bit32.bxor(d, k)))
    end
    return table.concat(result)
end

function crypto.encrypt(plaintext, hex_key)
    local key = hexToBytes(hex_key)
    local encrypted = xor(plaintext, key)
    return love.data.encode("string", "base64", encrypted)
end

function crypto.decrypt(base64_encoded, hex_key)
    local key = hexToBytes(hex_key)
    local encrypted = love.data.decode("string", "base64", base64_encoded)
    return xor(encrypted, key)
end

return crypto
