#!/usr/bin/env python3
import re
import os
import glob

VEINTAP_ASCII = r"""
██    ██ ███████  ██████  ██ ███    ██ ████████  █████  ██████  
██    ██ ██      ██       ██ ████   ██    ██    ██   ██ ██   ██ 
██    ██ █████   ██   ███ ██ ██ ██  ██    ██    ███████ ██████  
 ██  ██  ██      ██    ██ ██ ██  ██ ██    ██    ██   ██ ██   ██ 
  ████   ███████  ██████  ██ ██   ████    ██    ██   ██ ██   ██ 
                                                                
    VeinTap — Siphon the Lua Veins from Template Sludge!
"""

def print_banner():
    print(f"\033[95m{VEINTAP_ASCII}\033[0m")  # Purple ASCII art
    print("🩸 Starting the Lua vein tapping process...\n")

def extract_lua_blocks(template_path):
    with open(template_path, 'r') as file:
        content = file.read()
    lua_blocks = re.findall(r'<\?(.*?)\?>', content, re.DOTALL)
    if lua_blocks:
        print(f"🩻  Found {len(lua_blocks)} Lua block(s) in {os.path.basename(template_path)}")
    else:
        print(f"💤  No Lua blocks found in {os.path.basename(template_path)}")
    return '\n\n'.join(block.strip() for block in lua_blocks)

def compile_templates(input_dir, output_dir):
    print_banner()
    os.makedirs(output_dir, exist_ok=True)
    files_processed = 0
    for filepath in glob.glob(os.path.join(input_dir, '*.lua')):
        print(f"\n🔍  Tapping into {os.path.basename(filepath)}...")
        lua_code = extract_lua_blocks(filepath)
        if lua_code:
            filename = os.path.splitext(os.path.basename(filepath))[0] + '_compiled.lua'
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w') as out_file:
                out_file.write(lua_code)
            print(f"✅  Extracted Lua saved to {filename}")
            files_processed += 1
        else:
            print(f"⚠️  Skipping {os.path.basename(filepath)} (no Lua found)")
    print(f"\n🎉  VeinTap finished! {files_processed} file(s) compiled.\n")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='VeinTap: Extract Lua code blocks from template files.')
    parser.add_argument('--input-dir', required=True, help='Directory containing Lua templates.')
    parser.add_argument('--output-dir', required=True, help='Directory to output Lua files.')
    args = parser.parse_args()

    compile_templates(args.input_dir, args.output_dir)

