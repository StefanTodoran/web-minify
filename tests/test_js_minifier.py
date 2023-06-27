import unittest
from css_html_js_minify import js_minifier

class Test_JS_Minifier(unittest.TestCase):
    def test_js_no_break_inline_if(self):
        js_in = """
            function foo(bar) {
                if (bar)
                    console.log("baz");
            }
        """
        js_out = """function foo(bar){if(bar)console.log("baz");}"""
        self.assertEqual(js_minifier.js_minify(js_in), js_out)

    def test_js_try_catch(self):
        js_in = """
            try {
                console.log("foo");
            } 
            catch (error) {
                console.log("bar");
            }
        """
        js_out = """try{console.log("foo");}catch(error){console.log("bar");}"""
        self.assertEqual(js_minifier.js_minify(js_in), js_out)

if __name__ == "__main__":
    unittest.main()