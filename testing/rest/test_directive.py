import py

docutils = py.test.importorskip("docutils")
from _py.rest import directive, resthtml
from _py.rest.latex import process_rest_file
from testing.rest.setup import getdata

def setup_module(mod):
    mod.datadir = getdata()
    mod.testdir = py.test.ensuretemp("rest")

class TestGraphviz(object):
    def _graphviz_html(self):
        if not py.path.local.sysfind("dot"):
            py.test.skip("graphviz needed")
        directive.set_backend_and_register_directives("html")
        if not py.path.local.sysfind("svn"):
            py.test.skip("svn needed")
        txt = datadir.join("graphviz.txt")
        html = txt.new(ext="html")
        png = datadir.join("example1.png")
        resthtml.process(txt)
        assert html.check()
        assert png.check()
        html_content = html.read()
        assert png.basename in html_content
        html.remove()
        png.remove()
        
    def _graphviz_pdf(self):
        for exe in 'dot latex epstopdf ps2eps'.split():
            if  not py.path.local.sysfind(exe):
                py.test.skip("%r needed" %(exe,))

        directive.set_backend_and_register_directives("latex")
        txt = py.path.local(datadir.join("graphviz.txt"))
        pdf = txt.new(ext="pdf")
        dotpdf = datadir.join("example1.pdf")
        process_rest_file(txt)
        assert pdf.check()
        assert dotpdf.check()
        pdf.remove()
        dotpdf.remove()

    def test_graphviz(self):
        self._graphviz_html()
        self._graphviz_pdf()

def test_own_links():
    def callback(name, text):
        assert name == "foo"
        return "bar xyz", "http://codespeak.net/noclue"
    directive.register_linkrole("foo", callback)
    txt = testdir.join("link-role.txt")
    txt.write("""
:foo:`whatever`
""")
    html = txt.new(ext="html")
    resthtml.process(txt)
    assert html.check()
    htmlcontent = html.read()
    assert "http://codespeak.net/noclue" in htmlcontent
    assert "bar xyz" in htmlcontent