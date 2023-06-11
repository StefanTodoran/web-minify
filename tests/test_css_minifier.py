import unittest
from css_html_js_minify import css_minifier

class Test_CSS_Minifier(unittest.TestCase):
    def test_css_hex_condense_do_condense(self):
        css_in = "color: #aabbcc;"
        css_out = "color: #abc;"
        self.assertEqual(css_minifier.condense_hex_colors(css_in), css_out)

    def test_hex_condense_no_condense_six(self):
        css_in = "color: #abcabc;"
        css_out = "color: #abcabc;"
        self.assertEqual(css_minifier.condense_hex_colors(css_in), css_out)
    
    def test_hex_condense_no_condense_eight(self):
        css_in = "color: #aabbccdd;"
        css_out = "color: #aabbccdd;"
        self.assertEqual(css_minifier.condense_hex_colors(css_in), css_out)

if __name__ == "__main__":
    unittest.main()