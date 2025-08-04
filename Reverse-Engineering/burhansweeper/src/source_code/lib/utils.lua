utils = {}

-- https://love2d.org/wiki/love.math.random
function utils.shuffle (list)
	-- backward iteration from last to second element:
	for i = #list, 2, -1 do
		-- choose one of elements:
		local j = love.math.random(i) -- between 1 to i (both inclusive)
		-- replace both elements each other:
		list[i], list[j] = list[j], list[i]
	end
end


-- https://stackoverflow.com/questions/41942289/display-contents-of-tables-in-lua
function utils.tprint (tbl, indent)
	if not indent then indent = 0 end
	local toprint = string.rep(" ", indent) .. "{\r\n"
	indent = indent + 2 
	for k, v in pairs(tbl) do
		toprint = toprint .. string.rep(" ", indent)
		if (type(k) == "number") then
		toprint = toprint .. "[" .. k .. "] = "
		elseif (type(k) == "string") then
		toprint = toprint  .. k ..  "= "   
		end
		if (type(v) == "number") then
		toprint = toprint .. v .. ",\r\n"
		elseif (type(v) == "string") then
		toprint = toprint .. "\"" .. v .. "\",\r\n"
		elseif (type(v) == "table") then
		toprint = toprint .. utils.tprint(v, indent + 2) .. ",\r\n"
		else
		toprint = toprint .. "\"" .. tostring(v) .. "\",\r\n"
		end
	end
	toprint = toprint .. string.rep(" ", indent-2) .. "}"
	return toprint
end

return utils