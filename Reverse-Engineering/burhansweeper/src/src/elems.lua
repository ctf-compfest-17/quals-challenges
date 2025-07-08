local elems = {}
local Cell = require("cell")

local padx = 20
local pady = 20
local cellPad = 4
local innerPad = 30
local WHITE = {0.94, 0.94, 0.94}
local HOVER_COLOR = {0.5, 0.5, 0.5} 
local MINE_BG_COLOR = {0x8 / 255, 0x8 / 255, 0x8 / 255}

local HOVER_SPEED = 7 
local cellHoverProgress = {}
elems.revealedCells = {}


local function clamp(val, lower, upper)
    if lower > upper then lower, upper = upper, lower end 
    return math.max(lower, math.min(upper, val))
end


local function lerp(a, b, t)
    return a + (b - a) * t
end

local function getMinefieldSquareLayout(minefield)
    local windowW, windowH = love.graphics.getWidth(), love.graphics.getHeight()
    local maxSize = math.min(windowW - 2 * padx, windowH - 2 * pady)
    local squareOrigin = { x = padx, y = pady }

    local innerSize = maxSize - innerPad
    local mfW = minefield and minefield.width or 1 
    local mfH = minefield and minefield.height or 1

    local totalCellPaddingW = cellPad * (mfW > 0 and (mfW - 1) or 0)
    local totalCellPaddingH = cellPad * (mfH > 0 and (mfH - 1) or 0)

    local cellSize = (innerSize - totalCellPaddingW) / mfW
    if mfW == 0 then cellSize = 0 end 

    local gridStartX = squareOrigin.x + innerPad / 2
    local gridStartY = squareOrigin.y + innerPad / 2

    return {
        size = maxSize,
        origin = squareOrigin,
        cellSize = cellSize,
        gridStartX = gridStartX,
        gridStartY = gridStartY,
        mfW = mfW,
        mfH = mfH
    }
end

function elems.initializeHover(minefield)
    cellHoverProgress = {} 
    if not minefield or not minefield.width or not minefield.height then return end

    for mx = 1, minefield.width do
        cellHoverProgress[mx] = {}
        for my = 1, minefield.height do
            cellHoverProgress[mx][my] = 0 
        end
    end
end

function elems.drawMineBG()
    love.graphics.push()
    local layout = getMinefieldSquareLayout(nil) 
    love.graphics.setColor(MINE_BG_COLOR[1], MINE_BG_COLOR[2], MINE_BG_COLOR[3], 0.5)
    love.graphics.rectangle("fill", layout.origin.x, layout.origin.y, layout.size, layout.size, 20)
    love.graphics.pop()
end

function elems.updateHoverState(minefield, dt)
    if not minefield or not cellHoverProgress[1] then 
        return
    end

    local layout = getMinefieldSquareLayout(minefield)
    if layout.cellSize <= 0 then return end 

    local mouseX, mouseY = love.mouse.getPosition()
    local hoveredGridX, hoveredGridY = nil, nil

    if mouseX >= layout.gridStartX and mouseX < layout.gridStartX + layout.mfW * (layout.cellSize + cellPad) and
       mouseY >= layout.gridStartY and mouseY < layout.gridStartY + layout.mfH * (layout.cellSize + cellPad) then
        
        local relativeMouseX = mouseX - layout.gridStartX
        local relativeMouseY = mouseY - layout.gridStartY

        hoveredGridX = math.floor(relativeMouseX / (layout.cellSize + cellPad)) + 1
        hoveredGridY = math.floor(relativeMouseY / (layout.cellSize + cellPad)) + 1
        
        if relativeMouseX % (layout.cellSize + cellPad) > layout.cellSize then hoveredGridX = nil end
        if relativeMouseY % (layout.cellSize + cellPad) > layout.cellSize then hoveredGridY = nil end

        if hoveredGridX and (hoveredGridX < 1 or hoveredGridX > layout.mfW) then hoveredGridX = nil end
        if hoveredGridY and (hoveredGridY < 1 or hoveredGridY > layout.mfH) then hoveredGridY = nil end
    end
    
    for x = 1, layout.mfW do
        if not cellHoverProgress[x] then cellHoverProgress[x] = {} end
        for y = 1, layout.mfH do
            if cellHoverProgress[x][y] == nil then cellHoverProgress[x][y] = 0 end

            if x == hoveredGridX and y == hoveredGridY then
                cellHoverProgress[x][y] = math.min(1, cellHoverProgress[x][y] + dt * HOVER_SPEED)
            else
                cellHoverProgress[x][y] = math.max(0, cellHoverProgress[x][y] - dt * HOVER_SPEED)
            end
        end
    end
end

function elems.drawMines(minefield)
    love.graphics.push()

    local layout = getMinefieldSquareLayout(minefield)
    if layout.cellSize <= 0 then 
        love.graphics.pop()
        return
    end

    for x = 1, layout.mfW do
        for y = 1, layout.mfH do
            -- skip revealed cells
            if elems.revealedCells[x] and elems.revealedCells[x][y] then
                goto continue
            end


            local cellX = layout.gridStartX + (x - 1) * (layout.cellSize + cellPad)
            local cellY = layout.gridStartY + (y - 1) * (layout.cellSize + cellPad)

            local progress = 0
            if cellHoverProgress[x] and cellHoverProgress[x][y] then
                progress = cellHoverProgress[x][y]
            end

            local r, g, b
            if progress > 0 then
                r = lerp(WHITE[1], HOVER_COLOR[1], progress)
                g = lerp(WHITE[2], HOVER_COLOR[2], progress)
                b = lerp(WHITE[3], HOVER_COLOR[3], progress)
            else
                r, g, b = WHITE[1], WHITE[2], WHITE[3]
            end
            

            love.graphics.setColor(r, g, b)
            love.graphics.rectangle("fill", cellX, cellY, layout.cellSize, layout.cellSize, 3)

            ::continue::
        end
    end

    love.graphics.pop()
end

function elems.drawScore()
    love.graphics.push()

    love.graphics.setColor(1, 1, 1)

    local font = love.graphics.newFont(50)
    love.graphics.setFont(font)

    local text = tostring(CELLS_CLICKED) .. "/5"
    local textWidth = font:getWidth(text)
    local textHeight = font:getHeight()

    -- Centered horizontally, middle vertically using _G.X and _G.Y
    local x = _G.X * 0.823 - textWidth / 2
    local y = _G.Y * 0.5 - textHeight / 2

    love.graphics.print(text, x, y)

    love.graphics.pop()
end



function elems.mousePressedMines(minefield, x, y, button)
    local layout = getMinefieldSquareLayout(minefield)
    local offset = layout.cellSize + cellPad
    local col = clamp(math.floor((x - layout.gridStartX) / offset) + 1, 1, layout.mfW)
    local row = clamp(math.floor((y - layout.gridStartY) / offset) + 1, 1, layout.mfH)

    if elems.revealedCells[col] and elems.revealedCells[col][row] then
        return { safe = true, revealed = false }  
    end

    local curCell = minefield.cells[col][row]
    local isSafe = curCell.isSafe(curCell)

    if isSafe then
        elems.revealedCells[col] = elems.revealedCells[col] or {}
        elems.revealedCells[col][row] = true
        table.insert(_G.CLICKED, {col, row})
    end

    cellHoverProgress[col] = cellHoverProgress[col] or {}
    cellHoverProgress[col][row] = 0

    return {
        safe = isSafe,             
        revealed = true            
    }
end




return elems
