# Copyright © 2022 Novobi, LLC
# See LICENSE file for full copyright and licensing details.
from email.policy import default
from odoo import models, fields, api, exceptions
import datetime


class LibraryBook(models.Model):
    _inherit = "library.book"
    # _name = 'library.book'

    ISBN = fields.Char('ISBN', required = True)
    status = fields.Selection(selection = [('not published','Not Published'), ('available','Available'), ('borrowed','Borrowed'), ('lost','Lost')], 
                            required = True, default = 'available')

    current_borrower_id = fields.Many2one('res.partner', string = 'Current Borrower', tracking = True)
    date_return = fields.Date('Return Date')
    location_id = fields.Many2one('library.booklocation')
    url = fields.Char('URL', default="https://en.wikipedia.org/wiki/Book")

    
    def open_website_url(self):
        if(self.url):
            return {
                'type': 'ir.actions.act_url',
                'url': self.url,
                'target': 'new'
            }


    def library_borrower_action(self):
        form_popup_id = self.env.ref('novobi_henry_book.library_borrower_view_form').id
        self.ensure_one()
        res_id = self.env['library.book'].search([('ISBN', '=', self.ISBN)])
        print("___________OK____________",res_id.name)
        print("____________",form_popup_id)
        return {
            'res_model': 'library.borrower',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_ISBN': self.ISBN, 'default_book': self.name, 'default_borrower_ids': self.current_borrower_id, 'default_return_date': self.date_return},
            # 'res_id': res_id.id,
            'view_id': form_popup_id
        }
    
    @api.onchange('date_release')
    def _onchange_date_release(self):
        self.ensure_one()
        if(self.date_release and self.date_release > datetime.date.today()):
            self.status = 'not published'
        else:
            self.status = 'available'


    @api.constrains('ISBN')
    def _check_ISBN(self):
        ### Check for
        for record in self:
            isbn = record.env['library.book'].search([('ISBN', '=', record.ISBN), ('id', '!=', record.id)])
            print(isbn)
            if isbn:
                raise exceptions.ValidationError("ISBN already exists!")
