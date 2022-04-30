odoo.define('library_book.widget', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');
    var datepicker = require('web.datepicker'); 
    var dateToday = new Date();
    console.log("_____________________Widget_________COme")

    var RelativeTime = basic_fields.FieldDate.extend({
        
        init: function () {
            this._super.apply(this, arguments);
            // use the session timezone when formatting dates
            this.formatOptions.timezone = true;
            this.datepickerOptions = _.defaults(
                {},
                this.nodeOptions.datepicker || {},
                {

                    minDate: dateToday,
                }
            );
            
        },
    });

    field_registry.add('curdaywid', RelativeTime);

    return RelativeTime;
});