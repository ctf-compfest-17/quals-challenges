# JCGdec functions decompiler for IDA 7.5
# Hexrays decompiler and IDAPython plugins are needed
# Modified from:
# https://github.com/JCGdev/IDAFunctionsDecompiler/blob/main/functionDecompiler.py

import idautils
import idaapi
import idc
import ida_hexrays
import ida_lines
import ida_funcs
import ida_kernwin
import ida_ida

import sys
import os
import shutil

# --- CONFIGURATION ---
# PATH MUST BE SET.
# Windows users must use double backslashes for paths, e.g., "C:\\Users\\YourUser\\Desktop\\func_dumps"
outputPath: str = r"D:\CTF\Compfest 17\rev\real_ctf\solver\func_dumps"
# --- END CONFIGURATION ---

# We create a subdirectory for the function files
functionsPath: str = os.path.join(outputPath, "functions")

def main() -> None:
    """
    Main function to drive the decompilation process.
    """
    if outputPath == r"D:\RE\IDA_Dumps":
        IDAConsolePrint("[Warning] Output path is set to the default. Please change the 'outputPath' variable in the script.\n")
    
    if not checkOutputPath():
        # Stop if the output path cannot be created
        return

    if not initHexraysPlugin():
        # Stop if the decompiler is not available
        return

    IDAConsolePrint("[!] Starting decompilation...\n")

    realAndSanitizedFunctionNameMapping: dict = {}
    successful_decompilations: int = 0
    
    # Get a list of all functions to get a total count for progress indication
    all_functions = list(idautils.Functions())
    total_functions = len(all_functions)
    IDAConsolePrint(f"[*] Found {total_functions} functions to process.\n")

    for i, func_ea in enumerate(all_functions, 1):
        funcName = "N/A" # Default name in case of error
        try:
            # Get the function's name as it appears in IDA
            mangled_name: str = idc.get_func_name(func_ea)

            # Attempt to demangle the name for C++ functions
            # It uses the demangling options configured in IDA's settings
            demangled_name = idc.demangle_name(mangled_name, idc.get_inf_attr(idc.INF_LONG_DN))

            # Use the demangled name if available, otherwise fall back to the original name
            if demangled_name:
                funcName = demangled_name
            else:
                funcName = mangled_name
            
            sanitizedFuncName = sanitize_filename(funcName)
            
            # This mapping helps identify the real function name from its sanitized filename
            realAndSanitizedFunctionNameMapping[funcName] = sanitizedFuncName

            IDAConsolePrint(f"[{i}/{total_functions}] Decompiling --> {funcName}\n")

            if "long long" not in funcName:
                # Skip functions that don't contain "long long"
                continue

            # Decompile the function and get the pseudocode object
            pseudoCodeOBJ: idaapi.strvec_t = decompileFunction(func_ea)
            if not pseudoCodeOBJ:
                raise Exception("Decompilation returned empty object.")
                
            # Convert the pseudocode object to a clean string
            pseudoCodeString = pseudoCodeObjToString(pseudoCodeOBJ)

            # Save the pseudocode to its own file
            dumpPseudocodeToRespectiveFile(pseudoCodeString, sanitizedFuncName)
            
            successful_decompilations += 1
            del pseudoCodeOBJ

        except Exception as e:
            # Log any exceptions that occur during the process for a specific function
            exceptionLogger(e, funcName)

    IDAConsolePrint(f"[!] Successfully decompiled {successful_decompilations}/{total_functions} functions!\n")
    dumpToFileRealAndSanitizedFunctionNamesMapping(realAndSanitizedFunctionNameMapping)
    IDAConsolePrint(f"[!] Output saved to: {outputPath}\n")


def checkOutputPath() -> bool:
    """
    Checks and prepares the output directory. It will delete and recreate the
    directory if it already exists to ensure a clean slate.
    """
    try:
        if not os.path.exists(outputPath):
            os.makedirs(functionsPath)
        else:
            shutil.rmtree(outputPath)
            os.makedirs(functionsPath)
        return True
    except OSError as e:
        errorLogger(f"Could not create output directory '{outputPath}'. Error: {e}")
        return False


def initHexraysPlugin() -> bool:
    """
    Initializes the Hex-Rays decompiler plugin.
    Returns True on success, False on failure.
    """
    if not ida_hexrays.init_hexrays_plugin():
        errorLogger(f"Hex-Rays decompiler (version {ida_hexrays.get_hexrays_version()}) failed to initialize.")
        return False
    else:
        IDAConsolePrint(f"[*] Hex-Rays version {ida_hexrays.get_hexrays_version()} has been detected.\n")
        return True


def IDAConsolePrint(message: str) -> None:
    """
    Prints a message to the IDA Pro output window.
    """
    ida_kernwin.msg(message)


def sanitize_filename(stringToParse: str) -> str:
    """
    Removes or replaces characters from a string to make it a valid filename.
    This is especially important for demangled C++ names.
    """
    # Characters that are illegal or problematic in filenames on most OSes.
    # Includes characters commonly found in C++ demangled names like <, >, :, and whitespace.
    illegalChars = ('/', '\\', ':', '<', '>', '|', '?', '*', ' ', '&', '(', ')', "'", '`', '[', ']', '{', '}')
    parsedString: str = stringToParse

    for char in illegalChars:
        parsedString = parsedString.replace(char, "_")
        
    # Replace any remaining comma or period that might be problematic
    parsedString = parsedString.replace(",", "_")
    parsedString = parsedString.replace(".", "_")
    
    return parsedString


def decompileFunction(func_ea: int) -> idaapi.strvec_t:
    """
    Decompiles a single function at the given effective address (ea).
    """
    try:
        # Perform the decompilation
        decompiledFunc: ida_hexrays.cfuncptr_t = ida_hexrays.decompile(func_ea)
        if not decompiledFunc:
            return None
        
        # Get the pseudocode as a strvec_t object
        pseudoCodeOBJ: idaapi.strvec_t = decompiledFunc.get_pseudocode()
        return pseudoCodeOBJ

    except ida_hexrays.DecompilationFailure as e:
        # Re-raise the exception to be caught by the main loop
        raise Exception(f"Decompilation failed: {e}")


def pseudoCodeObjToString(pseudoCodeOBJ: idaapi.strvec_t) -> str:
    """
    Converts the decompiler's strvec_t object into a single, clean string.
    """
    convertedObj: str = ""
    for lineOBJ in pseudoCodeOBJ:
        # ida_lines.tag_remove strips away color codes and other formatting tags
        convertedObj += (ida_lines.tag_remove(lineOBJ.line) + "\n")
    return convertedObj


def dumpPseudocodeToRespectiveFile(pseudoCode: str, filename: str) -> None:
    """
    Writes the provided pseudocode string to a file in the functions directory.
    """
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_function"

    # To avoid "filename too long" errors, truncate if necessary
    max_len = 200 
    if len(filename) > max_len:
        filename = filename[:max_len]

    filename = filename[:filename.index("_std")]
        
    full_path = os.path.join(functionsPath, filename)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(pseudoCode)


def dumpToFileRealAndSanitizedFunctionNamesMapping(mapping: dict) -> None:
    """
    Saves a mapping of original function names to their sanitized filenames.
    """
    try:
        with open(os.path.join(outputPath, "1 - nameMap.txt"), "w", encoding="utf-8") as f:
            f.write("Original Function Name : Sanitized Filename\n")
            f.write("------------------------------------------\n")
            for key, value in mapping.items():
                f.write(f"{key} : {value}\n")
    except Exception as e:
        exceptionLogger(e, "NameMappingDump")


def exceptionLogger(exception: Exception, functionName: str = "N/A") -> None:
    """
    Logs exceptions to both the IDA console and a central error log file.
    """
    exc_info = sys.exc_info()
    error_message = f"[EXCEPTION on function '{functionName}']: '{str(exception)}' | Info: {exc_info[0].__name__ if exc_info[0] else 'N/A'}, {exc_info[1]}"
    IDAConsolePrint(error_message + "\n")
    try:
        with open(os.path.join(outputPath, "0 - ERROR_LOG.txt"), "a", encoding="utf-8") as f:
            f.write(error_message + "\n\n")
    except OSError:
        # This might happen if the output path is invalid
        IDAConsolePrint("[FATAL] Could not write to error log file!\n")


def errorLogger(message: str) -> None:
    """
    Logs a general error message (not an exception) to console and file.
    """
    IDAConsolePrint("[ERROR] " + message + "\n")
    try:
        with open(os.path.join(outputPath, "0 - ERROR_LOG.txt"), "a", encoding="utf-8") as f:
            f.write("[ERROR] " + message + "\n")
    except OSError:
        IDAConsolePrint("[FATAL] Could not write to error log file!\n")


if __name__ == "__main__":
    main()

