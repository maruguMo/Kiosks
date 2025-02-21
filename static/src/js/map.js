odoo.define('kiosks.map_widget', function (require) {
    "use strict";

    const AbstractField = require('web.AbstractField');
    const fieldRegistry = require('web.field_registry');

    const MapWidget = AbstractField.extend({
        template: 'kiosks.MapWidget',
        events: {
            'click': '_onClick',
        },

        init: function (parent, name, record, options) {
            this._super.apply(this, arguments);
            this.latitude = record.data.latitude || 0;
            this.longitude = record.data.longitude || 0;
        },

        start: function () {
            this._super.apply(this, arguments);
            this._initializeMap();
        },

        _initializeMap: function () {
            if (this.$el) {
                const map = L.map(this.$el[0]).setView([this.latitude, this.longitude], 13);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);

                if (this.latitude && this.longitude) {
                    L.marker([this.latitude, this.longitude]).addTo(map);
                }
            }
        },

        _onClick: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        },
    });

    fieldRegistry.add('osm_map', MapWidget);
    return MapWidget;
});