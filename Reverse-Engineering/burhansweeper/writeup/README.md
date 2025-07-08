# Writeup Burhansweeper

Game yang disediakan dibuat dengan LOVE2D yang merupakan game engine berbasis Lua. Source code sudah tersedia di dalam executable (tinggal dibuka pake WinRAR)

Buat nyari cell yang bener ada beberapa cara. Salah satunya yaitu mengganti warna cell ketika di-draw pada fungsi `elems.drawMines` trus tinggal pencet.

```lua
local Cell = require('cell')
local c = Cell::new(x, y)

if c.isSafe(c) then
    love.graphics.setColor(1,0,0)
else
    love.graphics.setColor(r,g,b)
end
love.graphics.rectangle("fill", cellX, cellY, layout.cellSize, layout.cellSize, 3)

```