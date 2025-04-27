#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime
import tree_sitter_lua as lua
from tree_sitter import Language, Parser
from colorama import Fore, Style, init
import yaml

init(autoreset=True)

# Load Lua grammar
LUA_LANGUAGE = Language(lua.language())
parser = Parser(LUA_LANGUAGE)

def print_logo():
    logo = r"""
   ____                 _     ____  _             
  / ___|_ __ ___  _ __ | |__ / ___|| | ___   __ _ 
 | |   | '__/ _ \| '_ \| '_ \\___ \| |/ _ \ / _` |
 | |___| | | (_) | |_) | | | |___) | | (_) | (_| |
  \____|_|  \___/| .__/|_| |_|____/|_|\___/ \__, |
                  |_|                       |___/ 
       C R Y P T   S L U I C E   -   Scrub the flow
    """
    print(Fore.GREEN + logo + Style.RESET_ALL)

class TaintAnalyzer:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.sources = config.get('sources', [])
        self.cleansers = config.get('cleansers', [])
        self.sinks = config.get('sinks', [])
        self.taint_map = {}
        self.taint_origins = {}
        self.taint_chains = {}
        self.sink_findings = []
        self.sink_danger = False

    def analyze_assignment(self, var_name, value_expr, line_number):
        if self.is_source(value_expr):
            self.taint_map[var_name] = True
            self.taint_origins[var_name] = line_number
            self.taint_chains[var_name] = [var_name]
            print(f"{Fore.YELLOW} Tainted source assigned to {var_name} from {value_expr} (Line {line_number})")
        elif self.is_cleanser(value_expr):
            self.taint_map[var_name] = False
            print(f"{Fore.CYAN} {var_name} cleansed by {value_expr}")
        elif self.is_tainted(value_expr):
            source_var = self.find_source_var(value_expr)
            self.taint_map[var_name] = True
            self.taint_origins[var_name] = self.taint_origins.get(source_var)
            self.taint_chains[var_name] = self.taint_chains.get(source_var, []) + [var_name]
            print(f"{Fore.MAGENTA} Taint propagated to {var_name} from {value_expr}")
        else:
            self.taint_map[var_name] = False
            print(f"{Fore.GREEN}✔️ {var_name} is untainted")

    def check_sink(self, func_name, args_expr, line_number):
        if func_name in self.sinks:
            if self.is_tainted(args_expr):
                source_var = self.find_source_var(args_expr)
                origin_line = self.taint_origins.get(source_var)
                chain = self.taint_chains.get(source_var, [])
                if chain and chain[-1] != args_expr:
                    chain = chain + [args_expr]
                self.sink_findings.append((source_var, origin_line, func_name, line_number, chain))
                print(f"{Fore.RED} Tainted data flows into sink: {func_name}({args_expr}) (Sink Line {line_number}, Source Line {origin_line})")
                print(f"{Fore.RED} Taint chain: {' → '.join(chain)}")
                self.sink_danger = True
            else:
                print(f"{Fore.BLUE} Safe sink usage: {func_name}({args_expr})")

    def is_source(self, expr):
        return any(source in expr for source in self.sources)

    def is_cleanser(self, expr):
        return any(cleanser in expr for cleanser in self.cleansers)

    def is_tainted(self, expr):
        return any(var in self.taint_map and self.taint_map[var] for var in expr.split())

    def find_source_var(self, expr):
        for var in expr.split():
            if var in self.taint_chains:
                return var
        return None

    def report(self, filepath):
        print(f"\n{Style.BRIGHT}{Fore.WHITE} Taint Summary for {filepath}:")
        print("-" * 50)
        if self.sink_findings:
            for source_var, source_line, sink_func, sink_line, chain in self.sink_findings:
                chain_str = " → ".join(chain)
                print(f"{Fore.RED} Source Line {source_line} → Sink '{sink_func}' at Line {sink_line}")
                print(f"{Fore.RED} Chain: {chain_str}")
                print("-" * 50)
            print(f"{Fore.RED}{Style.BRIGHT}❌ Danger: Sinks received tainted data in this file!")
        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}✅ Safe: No tainted data reached sinks in this file!")

def walk_tree(tree, code_bytes, analyzer):
    cursor = tree.walk()

    def recurse(node):
        if node.type == 'assignment_statement':
            var_node = node.child_by_field_name('name')
            expr_node = node.child_by_field_name('value')
            if var_node and expr_node:
                var_name = code_bytes[var_node.start_byte:var_node.end_byte].decode('utf8')
                value_expr = code_bytes[expr_node.start_byte:expr_node.end_byte].decode('utf8')
                line_number = var_node.start_point[0] + 1
                analyzer.analyze_assignment(var_name, value_expr, line_number)
        elif node.type == 'function_call':
            func_node = node.child_by_field_name('name')
            arg_nodes = node.child_by_field_name('arguments')
            if func_node and arg_nodes:
                func_name = code_bytes[func_node.start_byte:func_node.end_byte].decode('utf8')
                args_text = code_bytes[arg_nodes.start_byte:arg_nodes.end_byte].decode('utf8').strip('(').strip(')')
                line_number = func_node.start_point[0] + 1
                analyzer.check_sink(func_name, args_text, line_number)
        for child in node.children:
            recurse(child)
    recurse(cursor.node)

def analyze_file(filepath, analyzer):
    with open(filepath, 'r') as f:
        lua_code = f.read()
    tree = parser.parse(bytes(lua_code, 'utf8'))
    walk_tree(tree, bytes(lua_code, 'utf8'), analyzer)
    analyzer.report(filepath)

def analyze_directory(base_dir, config_path):
    total_files = 0
    dangerous_files = []
    safe_files = []
    detailed_chains = {}

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.lua'):
                total_files += 1
                filepath = os.path.join(root, file)
                print(f"\nAnalyzing {filepath}...")
                analyzer = TaintAnalyzer(config_path)
                analyze_file(filepath, analyzer)
                if analyzer.sink_danger:
                    dangerous_files.append(filepath)
                    chains = []
                    for source_var, source_line, sink_func, sink_line, chain in analyzer.sink_findings:
                        chains.append({
                            'source_var': source_var,
                            'source_line': source_line,
                            'sink_func': sink_func,
                            'sink_line': sink_line,
                            'taint_chain': chain
                        })
                    detailed_chains[filepath] = chains
                else:
                    safe_files.append(filepath)

    print(f"\n{Style.BRIGHT}{Fore.WHITE}\U0001F310 Global Summary:")
    print("-" * 40)
    print(f"{Fore.YELLOW}Total files analyzed: {total_files}")
    print(f"{Fore.RED}Dangerous files: {len(dangerous_files)}")
    for f in dangerous_files:
        print(f"  {Fore.RED}❌ {f}")
    print(f"{Fore.GREEN}Safe files: {len(safe_files)}")
    for f in safe_files:
        print(f"  {Fore.GREEN}✅ {f}")
    print("-" * 40)

    summary = {
        'total_files': total_files,
        'dangerous_files': dangerous_files,
        'safe_files': safe_files,
        'detailed_chains': detailed_chains
    }
    with open('taint_summary.json', 'w') as json_out:
        json.dump(summary, json_out, indent=4)
    print(f"{Fore.CYAN} JSON summary exported to taint_summary.json")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('taint_summary.md', 'w') as md_out:
        md_out.write(f"# Taint Analysis Summary\n\n")
        md_out.write(f"- **Project Directory:** `{base_dir}`\n")
        md_out.write(f"- **Analysis Time:** {timestamp}\n\n")
        md_out.write(f"**Total files analyzed:** {total_files}\n\n")
        md_out.write(f"## Dangerous Files ({len(dangerous_files)})\n")
        for f in dangerous_files:
            md_out.write(f"- ❌ `{f}`\n")
        if not dangerous_files:
            md_out.write(f"- ✅ None\n")
        md_out.write(f"\n## Safe Files ({len(safe_files)})\n")
        for f in safe_files:
            md_out.write(f"- ✅ `{f}`\n")
        if not safe_files:
            md_out.write(f"- ❌ None\n")
        if detailed_chains:
            md_out.write(f"\n## Taint Chains\n")
            for filepath, chains in detailed_chains.items():
                md_out.write(f"\n### `{filepath}`\n")
                for chain_info in chains:
                    chain_str = " → ".join(chain_info['taint_chain'])
                    md_out.write(f"- **Sink:** `{chain_info['sink_func']}` (Line {chain_info['sink_line']})\n")
                    md_out.write(f"  - **Source:** `{chain_info['source_var']}` (Line {chain_info['source_line']})\n")
                    md_out.write(f"  - **Taint Chain:** `{chain_str}`\n")
    print(f"{Fore.CYAN} Markdown summary exported to taint_summary.md")

if __name__ == "__main__":
    print_logo()
    if len(sys.argv) != 3:
        print("Usage: python main.py <base_directory> <config_file>")
        sys.exit(1)

    base_dir = sys.argv[1]
    config_file = sys.argv[2]
    analyze_directory(base_dir, config_file)

