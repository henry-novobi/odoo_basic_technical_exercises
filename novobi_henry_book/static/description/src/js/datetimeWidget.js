odoo.define('hr_attendance.widget', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');

    var RelativeTime = basic_fields.FieldDateTime.extend({
        _makeDatePicker: function () {
            this.formatOptions.timezone = true;
            this.datepickerOptions = _.defaults(
                {},
                this.nodeOptions.datepicker || {},
                {defaultDate: 0}
            );
            return new datepicker.DateWidget(this, this.datepickerOptions);
        },
    });

    field_registry.add('relative_time', RelativeTime);

    return RelativeTime;
});