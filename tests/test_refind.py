#!/bin/env python3

# MIT License
#
# Copyright (c) 2023 James Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from unittest.mock import patch
import os
import sys
import tempfile
from io import StringIO

THIS_FILE_PATH = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.join(THIS_FILE_PATH, '..'))
SOURCE_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'src'))

sys.path.insert(0, SOURCE_DIR)
from refind import find

class RefindTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        for i in range(4):
            with open(os.path.join(cls.tmpdir.name, f"file{i+1}.txt"), "w") as fd:
                fd.write(' ')
            dirname = os.path.join(cls.tmpdir.name, f"dir{i+1}")
            os.mkdir(dirname)
            for j in range(3):
                with open(os.path.join(dirname, f"dirfile{i+1}-{j+1}.txt"), 'w') as fd:
                    fd.write(' ')

    def setUp(self):
        self.old_dir = os.getcwd()
        os.chdir(self.tmpdir.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmpdir.cleanup()

    def tearDown(self):
        os.chdir(self.old_dir)

    def test_basic(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            '.', f'.{s}dir1', f'.{s}dir2', f'.{s}dir3', f'.{s}dir4',
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt', f'.{s}file4.txt',
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            f'.{s}dir2{s}dirfile2-1.txt', f'.{s}dir2{s}dirfile2-2.txt', f'.{s}dir2{s}dirfile2-3.txt',
            f'.{s}dir3{s}dirfile3-1.txt', f'.{s}dir3{s}dirfile3-2.txt', f'.{s}dir3{s}dirfile3-3.txt',
            f'.{s}dir4{s}dirfile4-1.txt', f'.{s}dir4{s}dirfile4-2.txt', f'.{s}dir4{s}dirfile4-3.txt',
            ''
        ])

    def test_print(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-print'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            '.', f'.{s}dir1', f'.{s}dir2', f'.{s}dir3', f'.{s}dir4',
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt', f'.{s}file4.txt',
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            f'.{s}dir2{s}dirfile2-1.txt', f'.{s}dir2{s}dirfile2-2.txt', f'.{s}dir2{s}dirfile2-3.txt',
            f'.{s}dir3{s}dirfile3-1.txt', f'.{s}dir3{s}dirfile3-2.txt', f'.{s}dir3{s}dirfile3-3.txt',
            f'.{s}dir4{s}dirfile4-1.txt', f'.{s}dir4{s}dirfile4-2.txt', f'.{s}dir4{s}dirfile4-3.txt',
            ''
        ])

    def test_filter_name(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-name', 'file?.txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt', f'.{s}file4.txt',
            ''
        ])

    def test_filter_not_name(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-not', '-name', 'file?.txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            '.', f'.{s}dir1', f'.{s}dir2', f'.{s}dir3', f'.{s}dir4',
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            f'.{s}dir2{s}dirfile2-1.txt', f'.{s}dir2{s}dirfile2-2.txt', f'.{s}dir2{s}dirfile2-3.txt',
            f'.{s}dir3{s}dirfile3-1.txt', f'.{s}dir3{s}dirfile3-2.txt', f'.{s}dir3{s}dirfile3-3.txt',
            f'.{s}dir4{s}dirfile4-1.txt', f'.{s}dir4{s}dirfile4-2.txt', f'.{s}dir4{s}dirfile4-3.txt',
            ''
        ])

    def test_filter_not_name_exclamation(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '!', '-name', 'file?.txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            '.', f'.{s}dir1', f'.{s}dir2', f'.{s}dir3', f'.{s}dir4',
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            f'.{s}dir2{s}dirfile2-1.txt', f'.{s}dir2{s}dirfile2-2.txt', f'.{s}dir2{s}dirfile2-3.txt',
            f'.{s}dir3{s}dirfile3-1.txt', f'.{s}dir3{s}dirfile3-2.txt', f'.{s}dir3{s}dirfile3-3.txt',
            f'.{s}dir4{s}dirfile4-1.txt', f'.{s}dir4{s}dirfile4-2.txt', f'.{s}dir4{s}dirfile4-3.txt',
            ''
        ])

    def test_filter_name_and_false(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-name', 'file?.txt', '-and', '-false'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [''])

    def test_name_and_true(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-name', 'file?.txt', '-a', '-true'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt', f'.{s}file4.txt',
            ''
        ])

    def test_name_and_type(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-name', 'dir*.txt', '-type', 'f'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            f'.{s}dir2{s}dirfile2-1.txt', f'.{s}dir2{s}dirfile2-2.txt', f'.{s}dir2{s}dirfile2-3.txt',
            f'.{s}dir3{s}dirfile3-1.txt', f'.{s}dir3{s}dirfile3-2.txt', f'.{s}dir3{s}dirfile3-3.txt',
            f'.{s}dir4{s}dirfile4-1.txt', f'.{s}dir4{s}dirfile4-2.txt', f'.{s}dir4{s}dirfile4-3.txt',
            ''
        ])

    def test_name_or_false(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-name', 'file?.txt', '-or', '-false'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt', f'.{s}file4.txt',
            ''
        ])

    def test_name_or_true(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-name', 'file?.txt', '-o', '-true'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            '.', f'.{s}dir1', f'.{s}dir2', f'.{s}dir3', f'.{s}dir4',
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt', f'.{s}file4.txt',
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            f'.{s}dir2{s}dirfile2-1.txt', f'.{s}dir2{s}dirfile2-2.txt', f'.{s}dir2{s}dirfile2-3.txt',
            f'.{s}dir3{s}dirfile3-1.txt', f'.{s}dir3{s}dirfile3-2.txt', f'.{s}dir3{s}dirfile3-3.txt',
            f'.{s}dir4{s}dirfile4-1.txt', f'.{s}dir4{s}dirfile4-2.txt', f'.{s}dir4{s}dirfile4-3.txt',
            ''
        ])

    def test_regex_default_type(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-regex', '.*[\\/]\([f-i]\+\)le[1-3].txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt',
            ''
        ])

    def test_regex_sed_type(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-regextype', 'sed', '-regex', '.*[\\/]\([f-i]\+\)le[1-3].txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt',
            ''
        ])

    def test_regex_egrep_type(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-regextype', 'egrep', '-regex', '.*[\\/]([f-i]+)le[1-3].txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt',
            ''
        ])

    def test_regex_py_type(self):
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-regextype', 'py', '-regex', '.*[\\/]([f-i]+)le[1-3].txt'])
            lines = fake_out.getvalue().split('\n')
        s = os.path.sep
        self.assertEqual(lines, [
            f'.{s}file1.txt', f'.{s}file2.txt', f'.{s}file3.txt',
            ''
        ])

    def test_path(self):
        s = os.path.sep
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-path', f'*{s}dir1{s}*.txt'])
            lines = fake_out.getvalue().split('\n')
        self.assertEqual(lines, [
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            ''
        ])

    def test_wholename(self):
        s = os.path.sep
        with patch('refind.find.sys.stdout', new = StringIO()) as fake_out:
            find.main(['.', '-wholename', f'*{s}dir1{s}*.txt'])
            lines = fake_out.getvalue().split('\n')
        self.assertEqual(lines, [
            f'.{s}dir1{s}dirfile1-1.txt', f'.{s}dir1{s}dirfile1-2.txt', f'.{s}dir1{s}dirfile1-3.txt',
            ''
        ])

if __name__ == '__main__':
    unittest.main()
