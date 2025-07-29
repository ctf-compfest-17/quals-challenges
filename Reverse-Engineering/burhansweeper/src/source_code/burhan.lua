local burhan = {}

function burhan.draw()
    love.graphics.push()

    local burhan = love.graphics.newImage("assets/burhan.png")
    local burhanImageData = love.image.newImageData("assets/burhan.png")
    local burhanW, burhanH = burhanImageData:getDimensions()
    X = love.graphics.getWidth()
    Y = love.graphics.getHeight()
    local scale = {
        x = 2.5,
        y = 2,
    }
    love.graphics.draw(burhan, 0, 0, 0, scale.x, scale.y)

    love.graphics.pop()
end

return burhan