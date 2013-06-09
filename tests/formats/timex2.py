#!/usr/bin/env python

import unittest
import xml.dom.minidom

from ternip.formats.timex2 import Timex2XmlDocument
from ternip.timex import Timex

class Timex2DocumentTest(unittest.TestCase):

    def test_strip_timexes(self):
        t = Timex2XmlDocument('<root>This is some <TIMEX2 attr="timex">annotated <TIMEX2>embedded annotated </TIMEX2>text</TIMEX2>.</root>')
        t.strip_timexes()
        self.assertEquals(str(t), xml.dom.minidom.parseString('<root>This is some annotated embedded annotated text.</root>').toxml())

    def test_reconcile_TIMEX(self):
        s = Timex2XmlDocument('<root>This is some annotated text.</root>')
        t = Timex(type='date')
        t.value = "20100710"
        t.mod = "BEFORE"
        t.freq = "1M"
        t.comment = "Test"
        s.reconcile([[('This', 'POS', set()), ('is', 'POS', set()), ('some', 'POS', {t}), ('annotated', 'POS', {t}), ('text', 'POS', {t}), ('.', 'POS', set())]])
        self.assertEquals(str(s), xml.dom.minidom.parseString('<root>This is <TIMEX2 VAL="20100710" MOD="BEFORE" COMMENT="Test" GRANUALITY="G1M">some annotated text</TIMEX2>.</root>').toxml())

    def test_reconcile_TIMEX_SET(self):
        s = Timex2XmlDocument('<root>This is some annotated text.</root>')
        t = Timex(type='set')
        t.value = "P6M"
        t.mod = "BEFORE"
        s.reconcile([[('This', 'POS', set()), ('is', 'POS', set()), ('some', 'POS', set([t])), ('annotated', 'POS', set([t])), ('text', 'POS', {t}), ('.', 'POS', set())]])
        self.assertEquals(str(s), xml.dom.minidom.parseString('<root>This is <TIMEX2 PERIODICITY="F6M" MOD="BEFORE" SET="YES">some annotated text</TIMEX2>.</root>').toxml())

    def test_timex_to_sents(self):
        d = Timex2XmlDocument('<root>This is <TIMEX2 VAL="20100701" MOD="BEFORE" NON_SPECIFIC="YES" GRANUALITY="G1D" COMMENT="Text">a timex</TIMEX2>.</root>')
        s = d.get_sents()
        t = s[0][2][2].pop()
        self.assertEquals(t.type, None)
        self.assertEquals(t.value, '20100701')
        self.assertEquals(t.mod, 'BEFORE')
        self.assertEquals(t.freq, "1D")
        self.assertEquals(t.comment, "Text")

    def test_timex_set_to_sents(self):
        d = Timex2XmlDocument('<root>This is <TIMEX2 PERIODICITY="F3D" SET="YES">a timex</TIMEX2>.</root>')
        s = d.get_sents()
        t = s[0][2][2].pop()
        self.assertEquals(t.type, 'set')
        self.assertEquals(t.value, 'P3D')


    def test_timex_to_sents_SET(self):
        d = Timex2XmlDocument('<root>This is <TIMEX2 SET="YES">a timex</TIMEX2>.</root>')
        s = d.get_sents()
        t = s[0][2][2].pop()
        self.assertEquals(t.type, 'set')