/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";


patch(ProductCard.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
});

patch(PosOrderline.prototype, {
    setup(vals) {
        super.setup(vals);
        this.discount = this.discount || 0;

    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            discount: this.discount || 0,
        };
    },
    setOptions(options) {
        var product = this.models["product.product"].getBy("id", this.product_id.id);
        if (this.config.allow_automatic_discount == true && product.discount != 0){
            this.set_discount(product.discount);
        }
        return super.setOptions(...arguments);
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                discount: { type: Number, optional: true },
            },
        },
    },
});