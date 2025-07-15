ICON_PATH = "assets/icon.jpg"
SCALE = 0.7

function love.conf(t)
    -- error handling for file
    local function fileExists(path)
        local f= io.open(path, "rb")
        if f then f:close() end
        return f ~= nil
    end

    t.window.title = "Burhansweeper"

    if fileExists(ICON_PATH) then
        t.window.icon = ICON_PATH
    end


    t.window.vsync = 1
    t.window.resizable = false
end