local Minefield = {}
local Cell = require("cell")

function Minefield:new(w, h, d)
    o = {
        width = w, 
        height = h,
        depth = d, 
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
            self.cells[x][y] = {}
            for z = 1, self.depth do
                self.cells[x][y][z] = Cell:new(x, y, z)
            end
        end
    end
end

return Minefield