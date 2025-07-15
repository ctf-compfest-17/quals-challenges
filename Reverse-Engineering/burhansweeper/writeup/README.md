# Writeup Burhansweeper

Game yang disediakan dibuat dengan [LOVE2D](https://love2d.org/wiki/Main_Page) yang merupakan game engine berbasis Lua. Kalau kita searching dikit, [sistem distribution game LOVE2D](https://love2d.org/wiki/Game_Distribution) mengandalkan source code/bytecode Lua dalam bentuk zip (file extension di rename menjadi `.love`) yang kemudian diappend kepada `love.exe`.

Jadi, kita tinggal extract saja file `game.exe` dan dari situ kita dapet bytecode Lua-nya. Selanjutnya, kita bisa decompile bytecode dengan tools seperti [LuaDec](https://luadec.metaworm.site/).

At first glance, kita bisa liat bahwa flagnya diencrypt dengan menggunakan key yang dihasilkan oleh fungsi `enc.hash`, 

```lua

-- fungsi local r1_0 menerima table of coordinates
local r0_0 = {}
local function r1_0(r0_9)
  table.sort(r0_9, function(r0_10, r1_10)
    if r0_10[1] ~= r1_10[1] then
      return r0_10[1] < r1_10[1]
    elseif r0_10[2] ~= r1_10[2] then
      return r0_10[2] < r1_10[2]
    else
      return r0_10[3] < r1_10[3]
    end
  end)
end

-- nanti koordinatnya dihash di fungsi ini
function r0_0.hash(r0_5)
  -- line: [37, 49] id: 5
  r1_0(r0_5)
  return love.data.encode("string", "base64", love.data.hash("sha384", r4_0(r0_5)))
end

-- fungsi decryptnya 
function r0_0.decrypt(r0_2, r1_2)
  return r3_0(love.data.decode("string", "base64", r0_2), r2_0(r1_2))
end

-- dari sini kita tau bahwa r2_1 itu flag yang decodednya, jadi kita tinggal copy logic decryption ke solver script
function r0_0.drawWin()
  local r0_1 = love.graphics.newFont(20)
  love.graphics.push()
  love.graphics.setColor(1, 1, 1)
  love.graphics.setFont(r0_1)
  local r2_1 = r0_0.decrypt(_G.WIN_MSG, r0_0.hash(_G.CLICKED))
  love.graphics.print(r2_1, (_G.X - r0_1:getWidth(r2_1)) / 2, (_G.Y - r0_1.getHeight(r0_1)) / 2)
  love.graphics.pop()
end

return r0_0
```

`enc.hash` menerima suatu table yang berisi koordinat jawaban yang benar. Logic pengecekan koordinat yang benar ada di `cell.lua` pada fungsi `cell.isSafe`,

Dari sini, solusi paling simple adalah untuk mengoverwrite file entrypoint `main.lua` dengan solver script karena sebenarnya LOVE2D gak peduli kalo file `.lua` nya berbentuk bytecode atau source code asli.

**`main.lua`**
```lua
_G.love = require('love')
local cell = require('cell')
local enc = require('enc')

_G.SIZE = 32
_G.WIN = "6ktTOQqLL6ltQzBqNFy0qsIixCMlCLeh3f1tQ2L+oPGSZAHv/f+UxeGEngJC0Fvb3XYuNnmvTM9tFXg6Wgb9"

function love.load()
    _G.t = {}
    for x = 1, _G.SIZE do
        for y = 1, _G.SIZE do
            for z = 1, _G.SIZE do
                local cell = cell:new(x, y, z)
                if cell:isSafe() then
                    table.insert(t, {x, y, z})
                end
            end
        end
    end

    local flag = enc.decrypt(_G.WIN, enc.hash(t))
    print(flag)
end

```

Jangan lupa untuk enable `console = true` di `conf.lua` agar mendapatkan output.

**`conf.lua`**
```lua
function love.conf(t)
    t.console = true
end
```


