# Copyright © 2022 Novobi, LLC
# See LICENSE file for full copyright and licensing details.
from email.policy import default
from odoo import models, fields, api, exceptions
from datetime import datetime,date
import logging
_logger = logging.getLogger(__name__)


class LibraryBook(models.Model):
    _inherit = ["library.book",'mail.thread', 'mail.activity.mixin']
    _name = 'library.book'

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
        self.ensure_one()
        form_popup_id = self.env.ref('novobi_henry_book.library_borrower_view_form').id
        # res_id = self.env['library.book'].search([('ISBN', '=', self.ISBN)])
        # print("___________OK____________",res_id.name)
        # print("____________",form_popup_id)
        return {
            'res_model': 'library.borrower',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_ISBN': self.ISBN, 'default_book': self.name, 'default_borrower_id': self.current_borrower_id.id, 'default_return_date': self.date_return},
            # 'res_id': res_id.id,
            'view_id': form_popup_id
        }

    def _change_book_status(self, status):
        for record in self:
            record.status = status
            record.current_borrower_id = False
            record.date_return = False
            print("Changed ", record.name ," to ", status)

    def book_returned_before_today(self):
        mail_template = self.env.ref('novobi_henry_book.email_template_librarians')
        overdue = self.env['library.book'].search(['&',('status', '=', "borrowed"),"|", ('date_return','<', date.today()), ('date_return','=', False)])
        ctx  = {'overdue_books_lst': overdue}
        email_values = {
            'email_from': "henry.le@novobi.com",
            'email_to': "henry.le@novobi.com",
            'email_cc': False,
            'recipient_ids': [],
            'partner_ids': [],
        }
        mail_template.with_context(**ctx).send_mail(self.env.user.company_id.id, force_send=True, email_values=email_values)
        _logger.info("Send email to Librarian")
                
    
    @api.onchange('date_release')
    def _onchange_date_release(self):
        self.ensure_one()
        if(self.date_release and self.date_release > date.today()):
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