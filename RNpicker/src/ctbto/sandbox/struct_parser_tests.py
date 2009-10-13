'''
Created on Sep 16, 2009

@author: aubert
'''

# unit tests part
import unittest
import sys
import os
import struct_parser
from struct_parser import Tokenizer, Compiler, CompilerError




def tests():
    suite = unittest.TestLoader().loadTestsFromModule(struct_parser)
    unittest.TextTestRunner(verbosity=2).run(suite)


class TestListParser(unittest.TestCase):
    
    
    def setUp(self):
        pass
        
    def test_simple_list_test(self):
        """ a first simple test with space and indent, dedents to eat"""
        
        the_string = "         [ 'a',     1.435, 3 ]"
        
        compiler = Compiler()
        
        the_result = compiler.compile_list(the_string)
        
        self.assertEqual(the_result, [ 'a', 1.435, 3])
    
    def test_imbricated_lists_test(self):
        """ multiple lists within lists """
        
        the_string = "[a,b, [1,2,3,4, [456,6,'absdef'], 234, 2.456 ], aqwe, done]"
                
        compiler = Compiler()
        
        the_result = compiler.compile_list(the_string)
        
        self.assertEqual(the_result, ['a','b', [1,2,3,4, [456,6,'absdef'], 234, 2.456 ], 'aqwe', 'done'])
  
    def test_list_without_bracket_test(self):
        """ simple list without bracket test """
        
        the_string = " 'a', b"
                
        compiler = Compiler()
        
        the_result = compiler.compile_list(the_string)
        
        self.assertEqual(the_result, ['a','b'])
    
    def test_list_without_bracket_test_2(self):
        """ list without bracket test with a list inside """
        the_string = " 'a', b, ['a thing', 2]"
                
        compiler = Compiler()
        
        the_result = compiler.compile_list(the_string)
        
        self.assertEqual(the_result, ['a','b', ['a thing', 2] ])
        
    def test_list_error(self):
        """ list error """
        the_string = "  a ]"
        
        compiler = Compiler()
        
        try:
            the_result = compiler.compile_list(the_string)
        except CompilerError, err:
            self.assertEqual(err.message, 'Expression "  a ]" cannot be converted as a list .')
      
    def test_special_character_in_string(self):
        """ simple list without bracket test """
        
        the_string = " 'a@', b"
                
        compiler = Compiler()
        
        the_result = compiler.compile_list(the_string)
        
        self.assertEqual(the_result, ['a@','b'])
        
    def test_list_error_2(self):
        """ unsupported char @ """
        the_string = " a @"
        
        compiler = Compiler()
        
        try:
            the_result = compiler.compile_list(the_string)
        except CompilerError, err:
            self.assertEqual(err.message, 'Unsupported token (type: @, value : OP) (line=3,col=1).')
        
        #self.assertRaises(CompilerError,compiler.compile_list,the_string)
    
    def test_simple_dict(self):
        """ simple dict """
        
        the_string = "{'a':1, b:2 }"
                
        compiler = Compiler()
        
        the_result = compiler.compile_dict(the_string)
        
        self.assertEqual(the_result, {'a':1, 'b':2 })
        
    def test_dict_with_list(self):
        """ list with dict """
        
        the_string = "{'a':1, b:[1,2,3,4,5] }"
                
        compiler = Compiler()
        
        the_result = compiler.compile_dict(the_string)
        
        self.assertEqual(the_result, {'a':1, 'b':[1,2,3,4,5]})
        
    def test_list_with_dict(self):
        """ list with dict """
        
        the_string = "['a',1,'b',{2:3,4:5} ]"
                
        compiler = Compiler()
        
        the_result = compiler.compile_list(the_string)
        
        self.assertEqual(the_result, ['a',1,'b',{2:3,4:5} ])
        
        
        
if __name__ == '__main__':
    tests()