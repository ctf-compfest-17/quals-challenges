local Minefield = {}
local Cell = require("cell")

function Minefield:new(w, h)
    o = {
        width = w, 
        height = h, 
        cells = {}
    } or {}
    setmetatable(o, self)
    self.__index = self
    return o
end

function Minefield:init(self)
    for x = 1, self.width do 
        self.cells[x] = {}
        for y = 1, self.height do
            self.cells[x][y] = Cell:new(x, y)
        end
    end
end

return Minefield