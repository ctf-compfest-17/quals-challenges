local GameOver = {}

function GameOver:new(o) 
    o = {}
    setmetatable(o, self)
    self.__index = self
    return o
end

