
coords = [ (14, 10), (20, 8), (9, 13), (13, 20), (12,5) ]

from hashlib import sha256

t1 = ','.join(map(lambda x: f'"{sha256(str(3 * x[0] + x[1]).encode()).hexdigest()}"', coords)) # plus
t2 = ','.join(map(lambda x: f'"{sha256(str(x[0] * x[1]).encode()).hexdigest()}"', coords)) # mult
t3 = ','.join(map(lambda x: f'"{sha256(str(x[0] - 2 * x[1]).encode()).hexdigest()}"', coords)) # minus


code = '''

function Cell.isSafe(self)
    local x = self.x 
    local y = self.y
    local t1 = {%s}
    local t2 = {%s}
    local t3 = {%s}

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

'''

print(code % (t1,t2,t3))
