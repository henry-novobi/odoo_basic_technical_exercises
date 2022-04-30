# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
from odoo import http
from odoo.http import request


class AddBookController(http.Controller):
    @http.route(['/library_book/add_new_book'], type='http', auth="public",csrf=False,methods=["POST"])
    def create_new_book(self, **kw):
        model_name = "library.book"
        in_status = ["not published", "available", "borrowed", "lost"]

        if kw:
            ISBN = kw['isbn']
            name = kw['name']
            short_name = kw['short_name']
            status = kw['status']
            if(status not in in_status):
                status = "available"

        isbn = request.env[model_name].sudo().search([("ISBN", "=", ISBN)])
        try:
            if(isbn):
                response = {
                    "status": "errorISBN",
                    "content": "ISBN already in database!"
                }
            elif status not in in_status:
                response = {
                    "status": "errorStatus",
                    "content": "Status must be in (\"not published\", \"available\", \"borrowed\", \"lost\")"
                }
            else:
                rec = request.env[model_name].sudo().create({
                    'ISBN': ISBN,
                    'name': name,
                    'short_name': short_name,
                    'status': status
                })
                response = {
                        "status": "done",
                        "content": "This book has been created"
                    }
        except:
            response = {
                "status": "error",
                "description": "System Error"
            }
        return json.dumps(response)

        