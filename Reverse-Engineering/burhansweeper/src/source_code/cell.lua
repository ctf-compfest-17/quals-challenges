local Cell = {}

function Cell:new(x, y)
    o = {
        x = x, 
        y = y,
        isRevealed = false,
        isFlagged = false,
    } or {}
    setmetatable(o, self)
    self.__index = self
    return o
end

function Cell.isSafe(self)
    local t1 = {"41cfc0d1f2d127b04555b7246d84019b4d27710a3f3aff6e7764375b1e06e05d","a21855da08cb102d1d217c53dc5824a3a795c1c1a44e971bf01ab9da3a2acbbf","d59eced1ded07f84c145592f65bdf854358e009c5cd705f5215bf18697fed103","3e1e967e9b793e908f8eae83c74dba9bcccce6a5535b4b462bd9994537bfe15c","3d914f9348c9cc0ff8a79716700b9fcd4d2f3e711608004eb8f138bcba7f14d9"} 
    local t2 = {"dbae772db29058a88f9bd830e957c695347c41b6162a7eb9a9ea13def34be56b","a512db2741cd20693e4b16f19891e72b9ff12cead72761fc5e92d2aaf34740c1","2ac878b0e2180616993b4b6aa71e61166fdc86c28d47e359d0ee537eb11d46d3","39bb88f40d3aa2b2fe9dea67be27c74765db0ebb3ff3cf8fb779af6319fa2045","39fa9ec190eee7b6f4dff1100d6343e10918d044c75eac8f9e9a2596173f80c9"} 
    local t3 = {"03b26944890929ff751653acb2f2af795cee38f937f379f52ed654a68ce91216","4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a","d3471dcc109cd382f5e09a64253c2219958b5f8f07371fba48ac81fed97bb18a","7526da843f9dcf11e0fdbc79999f907176e81c7295383cf7b9a35c1543065d03","d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35"} 

    a1 = love.data.encode("string", "hex", love.data.hash("sha256", tostring(3 * self.x + self.y)))
    a2 = love.data.encode("string", "hex", love.data.hash("sha256", tostring(self.x * self.y)))
    a3 = love.data.encode("string", "hex", love.data.hash("sha256", tostring(self.x - 2 * self.y)))

    local check1 = false
    local check2 = false
    local check3 = false

    for _, v in ipairs(t1) do
        if v == a1 then
            check1 = true
            break
        end
    end

    for _, v in ipairs(t2) do
        if v == a2 then
            check2 = true
            break
        end
    end

    for _, v in ipairs(t3) do
        if v == a3 then
            check3 = true
            break
        end
    end

    return check1 and check2 and check3     

end

return Cell