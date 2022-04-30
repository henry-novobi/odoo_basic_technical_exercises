# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('-standard', 'testhenry')
class TestTotalBook(TransactionCase):
    def test_total_book(self):
        #Set up location
        self.location0 = self.env['book.location'].create({
            'name': 'Location 0',
        })
        
        LibraryBook = self.env['library.book'].with_context(tracking_disable=True)        

        #Set up Book
        self.library_book0 = LibraryBook.create({
            'name': "This is Data 0",
            'ISBN': '001',
            'short_name': "Data 0",
            'location_id': self.location0.id
        })


        self.library_book1 = LibraryBook.create({
            'name': "This is Data 1",
            'ISBN': "002",
            'short_name': "Data 1",
            'location_id': self.location0.id
        })

        self.assertEqual(self.location0.total_books, 2, 'Yup. It\'s all corrects!')     