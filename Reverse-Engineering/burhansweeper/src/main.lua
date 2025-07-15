-- Function to ensure directory exists using os.execute
local function ensureDir(path)
    -- Use mkdir command (works on both Windows and Unix-like systems)
    if love.system.getOS() == "Windows" then
        os.execute('mkdir "' .. path:gsub("/", "\\") .. '" 2>nul')
    else
        os.execute('mkdir -p "' .. path .. '"')
    end
end

-- Function to get full path (relative to current working directory)
local function getFullPath(relativePath)
    return "./" .. relativePath
end

-- Function to copy non-Lua files as-is
local function copyFile(sourcePath, outputPath)
    local data = love.filesystem.read(sourcePath)
    if data then
        -- Ensure output directory exists
        local outputDir = outputPath:match("(.+)[/\\][^/\\]+$")
        if outputDir then
            ensureDir(getFullPath(outputDir))
        end
        
        -- Write file as-is
        local fullOutputPath = getFullPath(outputPath)
        local file = io.open(fullOutputPath, "wb")
        if file then
            file:write(data)
            file:close()
            print("Copied: " .. sourcePath .. " -> " .. outputPath)
            return true
        else
            print("Error copying to " .. fullOutputPath)
            return false
        end
    else
        print("Error reading " .. sourcePath)
        return false
    end
end

-- Function to process a single Lua file
local function processLuaFile(sourcePath, outputPath)
    local filefunc, err = love.filesystem.load(sourcePath)
    if not filefunc then
        print("Error loading " .. sourcePath .. ": " .. (err or "unknown error"))
        return false
    end
    
    local bytecode = string.dump(filefunc)
    
    -- Ensure output directory exists
    local outputDir = outputPath:match("(.+)[/\\][^/\\]+$")
    if outputDir then
        ensureDir(getFullPath(outputDir))
    end
    
    -- Write bytecode to file (keeping .lua extension)
    local fullOutputPath = getFullPath(outputPath)
    local file = io.open(fullOutputPath, "wb")
    if file then
        file:write(bytecode)
        file:close()
        print("Compiled: " .. sourcePath .. " -> " .. outputPath)
        return true
    else
        print("Error writing to " .. fullOutputPath)
        return false
    end
end

-- Function to recursively process directory
local function processDirectory(sourceDir, outputDir)
    local items = love.filesystem.getDirectoryItems(sourceDir)
    
    for _, item in ipairs(items) do
        local sourcePath = sourceDir .. "/" .. item
        local outputPath = outputDir .. "/" .. item
        
        local info = love.filesystem.getInfo(sourcePath)
        if info then
            if info.type == "directory" then
                -- Recursively process subdirectory
                ensureDir(getFullPath(outputPath))
                processDirectory(sourcePath, outputPath)
            elseif info.type == "file" and item:match("%.lua$") then
                -- Process Lua file
                processLuaFile(sourcePath, outputPath)
            elseif info.type == "file" then
                -- Copy other files as-is
                copyFile(sourcePath, outputPath)
            end
        end
    end
end

-- Main execution
local function compileToBytecode()
    local sourceDir = "source_code"
    local outputDir = "bytecode"
    
    -- Check if source directory exists
    if not love.filesystem.getInfo(sourceDir) then
        print("Source directory '" .. sourceDir .. "' not found!")
        return
    end
    
    -- Ensure output directory exists
    ensureDir(getFullPath(outputDir))
    
    print("Starting recursive compilation...")
    processDirectory(sourceDir, outputDir)
    print("Compilation complete!")
    
    -- Open Explorer window to the bytecode directory
    love.event.quit()
end

-- Run the compilation
compileToBytecode()
