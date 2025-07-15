local enc = {}
local crypto = require('crypto')
local function normalizeCoordinates(coords)
    table.sort(coords, function(a, b)
        if a[1] == b[1] then
            return a[2] < b[2]
        else
            return a[1] < b[1]
        end
    end)
end

local function coordsToString(coords)
    local parts = {}
    for _, pair in ipairs(coords) do
        table.insert(parts, string.format("%d,%d", pair[1], pair[2]))
    end
    return table.concat(parts, ";")
end

function enc.encrypt(coords)
    if #coords ~= 5 then
        return nil
    end

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


function enc.drawWin()
    local smallFont = love.graphics.newFont(20) 
    love.graphics.push()
    love.graphics.setColor(1, 1, 1)

    love.graphics.setFont(smallFont)

    local key = enc.encrypt(_G.CLICKED)
    local dec = crypto.decrypt(_G.WIN_MSG, key)

    local textWidth = smallFont:getWidth(dec)
    local textHeight = smallFont:getHeight()


    love.graphics.print(dec,
        (_G.X - textWidth) / 2,
        (_G.Y - textHeight) / 2
    )

    love.graphics.pop()
end


return enc
