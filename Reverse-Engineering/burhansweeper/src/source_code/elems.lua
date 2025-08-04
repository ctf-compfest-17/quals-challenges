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

local arrowButton = {}



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

-- stupid fucking thing
function elems.initUI()
    local offsetX = 25
    arrowButton = {
        left = {x = _G.X * 0.77 - offsetX, y = _G.Y * 0.6, w = 50, h = 50},
        right = {x = _G.X * 0.87 - offsetX, y = _G.Y * 0.6, w = 50, h = 50}
    }
end

function elems.initializeHover(minefield)
    cellHoverProgress = {} 
    if not minefield or not minefield.width or not minefield.height then return end

    for mx = 1, minefield.width do
        cellHoverProgress[mx] = {}
        for my = 1, minefield.height do
            cellHoverProgress[mx][my] = {}
            --depth change
            for mz = 1, minefield.depth do
                cellHoverProgress[mx][my][mz] = 0
            end
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
    if not minefield or not cellHoverProgress[_G.CURRENT_DEPTH] then 
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
    
    --depth change
    local layerHoverProgress = cellHoverProgress[_G.CURRENT_DEPTH] or {}
    for x = 1, layout.mfW do
        if not layerHoverProgress[x] then layerHoverProgress[x] = {} end
        for y = 1, layout.mfH do
            if layerHoverProgress[x][y] == nil then layerHoverProgress[x][y] = 0 end

            if x == hoveredGridX and y == hoveredGridY then
                layerHoverProgress[x][y] = math.min(1, layerHoverProgress[x][y] + dt * HOVER_SPEED)
            else
                layerHoverProgress[x][y] = math.max(0, layerHoverProgress[x][y] - dt * HOVER_SPEED)
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
    --depth change
    local currentRevealed = elems.revealedCells[_G.CURRENT_DEPTH] or {}
    local currentHover = cellHoverProgress[_G.CURRENT_DEPTH] or {}

    for x = 1, layout.mfW do
        for y = 1, layout.mfH do
            if currentRevealed[x] and currentRevealed[x][y] then
                goto continue
            end

            local cellX = layout.gridStartX + (x - 1) * (layout.cellSize + cellPad)
            local cellY = layout.gridStartY + (y - 1) * (layout.cellSize + cellPad)

            local progress = 0
            if currentHover[x] and currentHover[x][y] then
                progress = currentHover[x][y]
            end

            local r, g, b
            local curCell = Cell:new(x, y, _G.CURRENT_DEPTH)
            local isSafe = curCell.isSafe(curCell)



            if progress > 0 then
                r = lerp(WHITE[1], HOVER_COLOR[1], progress)
                g = lerp(WHITE[2], HOVER_COLOR[2], progress)
                b = lerp(WHITE[3], HOVER_COLOR[3], progress)
            else
                r, g, b = WHITE[1], WHITE[2], WHITE[3]
            end

            -- if isSafe then
            --     r, g, b = 1, 0, 0 
            -- else
            --     r, g, b = WHITE[1], WHITE[2], WHITE[3]
            -- end
            
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

    local text = tostring(CELLS_CLICKED) .. "/" .. tostring(_G.TOTAL_SAFE)
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

    -- ignore outside grid click
    local gridTotalWidth = layout.mfW * layout.cellSize + (layout.mfW - 1) * cellPad
    local gridTotalHeight = layout.mfH * layout.cellSize + (layout.mfH - 1) * cellPad

    if x < layout.gridStartX or x > layout.gridStartX + gridTotalWidth or
       y < layout.gridStartY or y > layout.gridStartY + gridTotalHeight then
        return { safe = false, revealed = false } 
    end


    local col = clamp(math.floor((x - layout.gridStartX) / offset) + 1, 1, layout.mfW)
    local row = clamp(math.floor((y - layout.gridStartY) / offset) + 1, 1, layout.mfH)

    -- ignore click padding
    local relativeMouseX = x - layout.gridStartX
    local relativeMouseY = y - layout.gridStartY
    if relativeMouseX % offset > layout.cellSize or relativeMouseY % offset > layout.cellSize then
        return { safe = false, revealed = false }
    end


    local z = _G.CURRENT_DEPTH
    elems.revealedCells[z] = elems.revealedCells[z] or {}
    elems.revealedCells[z][col] = elems.revealedCells[z][col] or {}

    if elems.revealedCells[z][col][row] then
        return { safe = true, revealed = false }  
    end

    local curCell = minefield.cells[col][row][z]
    local isSafe = curCell.isSafe(curCell)

    if isSafe then
        elems.revealedCells[z][col][row] = true
        table.insert(_G.CLICKED, {col, row, z})
    end

    cellHoverProgress[z] = cellHoverProgress[z] or {}
    cellHoverProgress[z][col] = cellHoverProgress[z][col] or {}
    cellHoverProgress[z][col][row] = 0

    return {
        safe = isSafe,             
        revealed = true            
    }
end

--depth change
function elems.drawDepth()
    love.graphics.push()
    local font = love.graphics.newFont(25)
    love.graphics.setFont(font)
    love.graphics.setColor(1,1,1)

    -- text
    local text = "Z:" .. tostring(_G.CURRENT_DEPTH)
    local textWidth = font:getWidth(text)
    love.graphics.print(text, _G.X * 0.823 - textWidth/2, _G.Y *0.7)

    -- arrows
    love.graphics.polygon("fill", arrowButton.left.x, arrowButton.left.y + arrowButton.left.h/2, arrowButton.left.x + arrowButton.left.w, arrowButton.left.y, arrowButton.left.x + arrowButton.left.w, arrowButton.left.y + arrowButton.left.h)
    love.graphics.polygon("fill", arrowButton.right.x + arrowButton.right.w, arrowButton.right.y + arrowButton.right.h/2, arrowButton.right.x, arrowButton.right.y, arrowButton.right.x, arrowButton.right.y + arrowButton.right.h)
    love.graphics.pop()
end

function elems.mousePressedDepth(x,y)
    if x > arrowButton.left.x and x < arrowButton.left.x + arrowButton.left.w and y > arrowButton.left.y and y < arrowButton.left.y + arrowButton.left.h then
        return "left"
    end
    if x > arrowButton.right.x and x < arrowButton.right.x + arrowButton.right.w and y > arrowButton.right.y and y < arrowButton.right.y + arrowButton.right.h then
        return "right"
    end
    return nil
end

return elems
