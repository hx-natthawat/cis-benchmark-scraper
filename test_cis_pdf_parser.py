#!/usr/bin/env python3

import unittest
import sys
import logging
import re
from cis_pdf_parser import CISBenchmarkParser

class TestCISBenchmarkParser(unittest.TestCase):
    def setUp(self):
        """Setup test environment"""
        self.parser = CISBenchmarkParser()

    def test_extract_benchmark_name(self):
        """Test benchmark name extraction"""
        test_cases = [
            {
                'cover_text': 'CIS Apache Tomcat 8 Benchmark',
                'expected_name': 'Apache Tomcat 8'
            },
            {
                'cover_text': 'CIS Red Hat Enterprise Linux 7 Benchmark',
                'expected_name': 'Red Hat Enterprise Linux 7'
            },
            {
                'cover_text': 'CIS Microsoft Windows Server 2019 Benchmark (L1) Automated',
                'expected_name': 'Microsoft Windows Server 2019'
            }
        ]

        for case in test_cases:
            with self.subTest(cover_text=case['cover_text']):
                extracted_name = self.parser.extract_benchmark_name(case['cover_text'])
                self.assertIsNotNone(extracted_name)
                self.assertIn(case['expected_name'], extracted_name)

    def test_get_parsing_pattern(self):
        """Test regex pattern selection"""
        test_cases = [
            {
                'benchmark_name': 'CIS Apache Tomcat 8 Benchmark',
                'expected_pattern_contains': r'(Automated)|(Manual)|(Scored)|(Not Scored)'
            },
            {
                'benchmark_name': 'CIS Red Hat Enterprise Linux 7 Benchmark',
                'expected_pattern_contains': r'(Automated)|(Manual)'
            },
            {
                'benchmark_name': 'CIS Microsoft Windows Server 2019 Benchmark',
                'expected_pattern_contains': r'\(((L[12])|(NG))\)'
            }
        ]

        for case in test_cases:
            with self.subTest(benchmark_name=case['benchmark_name']):
                pattern = self.parser.get_parsing_pattern(case['benchmark_name'])
                self.assertIsNotNone(pattern)
                self.assertTrue(re.search(case['expected_pattern_contains'], pattern), 
                    f"Pattern {pattern} does not contain expected pattern")

    def test_invalid_benchmark_name(self):
        """Test handling of invalid benchmark names"""
        with self.assertRaises(ValueError):
            self.parser.get_parsing_pattern("Unknown Benchmark")

    def test_argument_parser(self):
        """Test command-line argument parsing"""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--pdf_file", type=str, required=True)
        parser.add_argument("--out_file", type=str, required=True)
        parser.add_argument("-l", "--log-level", type=str, default="INFO")

        # Test valid argument parsing
        args = parser.parse_args([
            '--pdf_file', 'test.pdf', 
            '--out_file', 'output.csv'
        ])
        
        self.assertEqual(args.pdf_file, 'test.pdf')
        self.assertEqual(args.out_file, 'output.csv')
        self.assertEqual(args.log_level, 'INFO')

    def test_logging_configuration(self):
        """Test logging configuration"""
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        for level_name, level_value in log_levels.items():
            parser = CISBenchmarkParser(level_name)
            self.assertEqual(parser.logger.level, level_value, 
                f"Logging level mismatch for {level_name}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
