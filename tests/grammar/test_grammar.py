import pytest
import numpy as np

import tatsu

import logging

class TestGrammar():
    class FBXSemantics(object):

        logger = logging.getLogger(__name__)

        def int_64(self, ast):
            self.logger.debug(ast.value)
            return np.frombuffer(ast.value, dtype=np.int_)

        def int_32(self, ast):
            print(ast.value)
            return np.frombuffer(ast.value, dtype=np.intc)
        
        def int_8(self, ast):
            self.logger.debug(ast.value)
            return np.frombuffer(ast.value, dtype=np.byte)

        def char(self, ast):
            self.logger.debug(ast.value)
            return np.frombuffer(ast.value, dtype=np.char)

        def _default(self, ast, *args, **kwargs):
            pass

    logger = logging.getLogger(__name__)

    def test_grammar(self):
        grammar = ""

        with open('grammar/fbx_binary.ebnf') as ebnf:
            grammar = ebnf.read()

        parser = tatsu.compile(grammar, semantics=self.FBXSemantics())

        with open('tests/resources/Zombie.binary.fbx', 'rb') as zombie:
            model = parser.parse(zombie.read(32).decode(encoding='ascii', errors='ignore'))

            print(model)

if __name__ == "__main__":
    TestGrammar().test_grammar()