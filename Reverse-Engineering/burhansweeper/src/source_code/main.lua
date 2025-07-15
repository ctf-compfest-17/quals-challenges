_G.love = require("love")

local Cell          = require("cell")
local Minefield     = require("minefield")
local utils         = require("lib.utils")
local elems         = require("elems")
local burhan        = require("burhan")
local enc           = require("enc")
local crypto        = require("crypto")

_G.SCREEN_W, _G.SCREEN_H = love.window.getDesktopDimensions()
_G.SCREEN_SCALE = 0.7
_G.CLICKED = {}
_G.WIN_MSG = "8Bn8SoOsBMEKAs9oQfh+S+nZij0i3lMabXGF9j9rycJFF6TIzC/V11eObZlwK5417BumVK6lRMJVPI9eXaV7WZGisHsjmgsKejna7RI/wPFGRPLc+xKo2CSqDv9wfdZlgkHv"

CELLS_CLICKED = 0
GLOBAL_TIME = 0
TIMEOUT = 0
hitMine = false

function love.load()
    love.window.setMode(SCREEN_W*SCREEN_SCALE-200, SCREEN_H*SCREEN_SCALE, {vsync = true, msaa=15}) 
    _G.X, _G.Y = love.graphics.getWidth(), love.graphics.getHeight()

    -- initialize hover state
    mf = Minefield:new(30, 30)
    mf:init(mf)
    elems.initializeHover(mf)
    -- initialize shader
    bgShader = love.graphics.newShader("shaders/bgshader.frag")
    
end 

function love.update(dt)
    GLOBAL_TIME = GLOBAL_TIME + dt
    elems.updateHoverState(mf, dt)

    if hitMine == true then
        TIMEOUT = TIMEOUT + dt
        if TIMEOUT > 1 then
            love.event.quit()
        end
    else
        TIMEOUT = 0
    end

end

function love.draw()

    -- validate shader
    if bgShader then 
        love.graphics.setShader(bgShader)
        bgShader:send("u_time", GLOBAL_TIME)
        bgShader:send("u_resolution", {_G.X, _G.Y})
        love.graphics.rectangle("fill", 0,0, _G.X, _G.Y)
        love.graphics.setShader()
    else
        love.graphics.setBackgroundColor(0x20/255, 0x20/255, 0x20/255)
        love.graphics.clear(love.graphics.getBackgroundColor())
    end

    elems.drawScore()
    elems.drawMineBG()
    elems.drawMines(mf)
    love.graphics.setColor(1,1,1)

    if hitMine then
        burhan.draw()
    end

    if CELLS_CLICKED == 5 then
        love.graphics.setColor(0,0,0)
        love.graphics.rectangle("fill", 0,0,_G.X,_G.Y)
        enc.drawWin()
    end

end

function love.mousepressed(x, y, button)
    if button == 1 and not hitMine then
        local res = elems.mousePressedMines(mf, x, y, button)

        if res.revealed then
            CELLS_CLICKED = CELLS_CLICKED + 1

            if not res.safe then
                hitMine = true
            end
        end



        print("CELLS_CLICKED:", CELLS_CLICKED)
        print("hitMine:", hitMine)
    end
end



