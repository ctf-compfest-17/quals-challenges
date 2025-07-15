local enc = {}

local function normalizeCoordinates(coords)
    table.sort(coords, function(a, b)
        if a[1] ~= b[1] then
            return a[1] < b[1] 
        elseif a[2] ~= b[2] then
            return a[2] < b[2] 
        else
            return a[3] < b[3] 
        end
    end)
end

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

local function coordsToString(coords)
    local parts = {}
    for _, v in ipairs(coords) do
        table.insert(parts, string.format("%d,%d,%d", v[1], v[2], v[3]))
    end
    return table.concat(parts, ";")
end

function enc.hash(coords)
    -- if #coords ~= 5 then
    --     return nil
    -- end

    normalizeCoordinates(coords)
    local str = coordsToString(coords)

    local hash = love.data.hash("sha384", str)
    local encoded = love.data.encode("string", "base64", hash)

    return encoded
end

function enc.verify(coords, hashToCompare)
    normalizeCoordinates(coords)
    local str = coordsToString(coords)

    local hash = love.data.hash("sha384", str)
    local encoded = love.data.encode("string", "base64", hash)

    return encoded == hashToCompare
end

function enc.encrypt(plaintext, hex_key)
    local key = hexToBytes(hex_key)
    local encrypted = xor(plaintext, key)
    return love.data.encode("string", "base64", encrypted)
end

function enc.decrypt(base64_encoded, hex_key)
    local key = hexToBytes(hex_key)
    local encrypted = love.data.decode("string", "base64", base64_encoded)
    return xor(encrypted, key)
end

function enc.drawWin()
    local smallFont = love.graphics.newFont(20) 
    love.graphics.push()
    love.graphics.setColor(1, 1, 1)

    love.graphics.setFont(smallFont)

    local key = enc.hash(_G.CLICKED)
    local dec = enc.decrypt(_G.WIN_MSG, key)

    local textWidth = smallFont:getWidth(dec)
    local textHeight = smallFont:getHeight()

    love.graphics.print(dec,
        (_G.X - textWidth) / 2,
        (_G.Y - textHeight) / 2
    )

    love.graphics.pop()
end

return enc