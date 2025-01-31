from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import sys
sys.path.append('src/pegen/generate')
from main import main as pegen_main

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        self.version = version
        self.build_data = build_data
        self.build()

    def build(self):
        sys.argv = ['pegen', '--quiet', '-o', 'src/pegen/ast/parser.py', 'python.gram']
        pegen_main() 