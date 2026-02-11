/** @odoo-module **/
/** (C) 2025 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com **/

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { floatIsZero } from "@web/core/utils/numbers";

function _newRandomRewardCode() {
    return (Math.random() + 1).toString(36).substring(3);
}

patch(PosOrder.prototype, {
    _getCheapestLine() {
        const product_ids = this.lines.filter(line => line.reward_id && line.raw?.product_id_ref).map(line => line.raw.product_id_ref);
        for (let j = 0; j < this.lines.length; j++) {
            if (product_ids.includes(this.lines[j].product_id.id)) {
                if (this.lines[j].qty > 1) {
                    const index = product_ids.indexOf(this.lines[j].product_id.id);
                    if (index !== -1) product_ids.splice(index, 1);
                }
                if (this.lines[j].raw?.product_id_ref) product_ids.push(this.lines[j].raw.product_id_ref);
            }
        }
        const filtered_lines = this.get_orderlines().filter((line) => !line.comboParent && !line.reward_id && line.get_quantity && !product_ids.includes(line.product_id.id));
        return filtered_lines.toSorted((lineA, lineB) => lineA.getComboTotalPrice() - lineB.getComboTotalPrice())[0];
    },
    _applyReward(reward, coupon_id, args) {
        if (this._getRealCouponPoints(coupon_id) < reward.required_points) {
            return _t("There are not enough points on the coupon to claim this reward.");
        }
        if (reward.is_global_discount) {
            const globalDiscountLines = this._getGlobalDiscountLines();
            if (globalDiscountLines.length) {
                const rewardId = globalDiscountLines[0].reward_id;
                if (rewardId != reward.id && rewardId.discount >= reward.discount) {
                    return _t("A better global discount is already applied.");
                } else if (rewardId != rewardId.id) {
                    for (const line of globalDiscountLines) {
                        line.delete();
                    }
                }
            }
        }
        args = args || {};
        const rewardLines = this._getRewardLineValues({
            reward: reward,
            coupon_id: coupon_id,
            product: args["product"] || null,
            price: args["price"] || null,
            quantity: args["quantity"] || null,
            cost: args["cost"] || null,
        });
        if (!Array.isArray(rewardLines)) {
            return rewardLines;
        }
        if (!rewardLines.length) {
            return _t("The reward could not be applied.");
        }
        for (const rewardLine of rewardLines) {
            const prepareRewards = {
                ...rewardLine,
                reward_id: rewardLine.reward_id,
                coupon_id: this.models["loyalty.card"].get(rewardLine.coupon_id),
                tax_ids: rewardLine.tax_ids.map((tax) => ["link", tax]),
                product_id_ref: rewardLine.product_id_ref,
            };
            this.models["pos.order.line"].create({
                ...prepareRewards,
                order_id: this,
                price_type: "manual",
            });
        }
        return true;
    },
    _getDiscountableOnCheapest(reward) {
        const cheapestLine = this._getCheapestLine();
        if (!cheapestLine) {
            return { discountable: 0, discountablePerTax: {} };
        }
        const taxKey = cheapestLine.tax_ids.map((t) => t.id);
        return {
            discountable: cheapestLine.getComboTotalPriceWithoutTax(),
            discountablePerTax: Object.fromEntries([
                [taxKey, cheapestLine.getComboTotalPriceWithoutTax()],
            ]),
            product_id_ref: cheapestLine.product_id.id,
        };
    },
    _getRewardLineValuesDiscount(args) {
        for (let j = 0; j < this.lines.length; j++) {
                    if (this.lines[j].discount == 100 && this.lines[j].price_subtotal == 0) {
                        this.lines[j].set_discount(0);
                    }
                }
        const reward = args["reward"];
        const coupon_id = args["coupon_id"];
        const rewardAppliesTo = reward.discount_applicability;
        let getDiscountable;
        if (rewardAppliesTo === "order") {
            getDiscountable = this._getDiscountableOnOrder.bind(this);
        } else if (rewardAppliesTo === "cheapest") {
            getDiscountable = this._getDiscountableOnCheapest.bind(this);
        } else if (rewardAppliesTo === "specific") {
            getDiscountable = this._getDiscountableOnSpecific.bind(this);
        }
        if (!getDiscountable) {
            return _t("Unknown discount type");
        }
        let { discountable, discountablePerTax } = getDiscountable(reward);
        let { product_id_ref } = getDiscountable(reward);
        discountable = Math.min(this.get_total_with_tax(), discountable);
        if (floatIsZero(discountable)) {
            return [];
        }
        let maxDiscount = reward.discount_max_amount || Infinity;
        if (reward.discount_mode === "per_point") {
            const points = ["ewallet", "gift_card"].includes(reward.program_id.program_type)
                ? this._getRealCouponPoints(coupon_id)
                : Math.floor(this._getRealCouponPoints(coupon_id) / reward.required_points) *
                  reward.required_points;
            maxDiscount = Math.min(maxDiscount, reward.discount * points);
        } else if (reward.discount_mode === "per_order") {
            maxDiscount = Math.min(maxDiscount, reward.discount);
        } else if (reward.discount_mode === "percent") {
            maxDiscount = Math.min(maxDiscount, discountable * (reward.discount / 100));
        }
        const rewardCode = _newRandomRewardCode();
        let pointCost = reward.clear_wallet
            ? this._getRealCouponPoints(coupon_id)
            : reward.required_points;
        if (reward.discount_mode === "per_point" && !reward.clear_wallet) {
            pointCost = Math.min(maxDiscount, discountable) / reward.discount;
        }
        const discountProduct = reward.discount_line_product_id;
        if (["ewallet", "gift_card"].includes(reward.program_id.program_type)) {
            const new_price = compute_price_force_price_include(
                discountProduct.taxes_id,
                -Math.min(maxDiscount, discountable),
                discountProduct,
                this.config._product_default_values,
                this.company,
                this.currency,
                this.models
            );
            return [
                {
                    product_id: discountProduct,
                    price_unit: new_price,
                    qty: 1,
                    reward_id: reward,
                    is_reward_line: true,
                    coupon_id: coupon_id,
                    points_cost: pointCost,
                    reward_identifier_code: rewardCode,
                    tax_ids: discountProduct.taxes_id,
                },
            ];
        }
        const discountFactor = discountable ? Math.min(1, maxDiscount / discountable) : 1;
        const result = Object.entries(discountablePerTax).reduce((lst, entry) => {
            if (!entry[1]) {
                return lst;
            }
            let taxIds = entry[0] === "" ? [] : entry[0].split(",").map((str) => parseInt(str));
            taxIds = this.models["account.tax"].filter((tax) => taxIds.includes(tax.id));
            if (reward.dirtcly_product_line) {
                this.lines.forEach(line => line.product_id.id === product_id_ref && (line.apply_discount = true));
                const applyDiscounts = (lineCount) => {
                    this.lines.filter(line => line.apply_discount).sort((a, b) => a.getComboTotalPrice() - b.getComboTotalPrice()).slice(0, lineCount).forEach(line => line.set_discount(100));
                };
                const lineCount = this.lines.length === 2 || this.lines.length === 3 ? 1 : this.lines.length <= 5 ? 2 : 3;
                if (lineCount > 0) {applyDiscounts(lineCount);}
            } else {
                lst.push({
                product_id: discountProduct,
                product_id_ref: product_id_ref,
                price_unit: -(Math.min(this.get_total_with_tax(), entry[1]) * discountFactor),
                qty: 1,
                reward_id: reward,
                is_reward_line: true,
                coupon_id: coupon_id,
                points_cost: 0,
                reward_identifier_code: rewardCode,
                tax_ids: taxIds,
                });
            }
            return lst;
        }, []);
        if (result.length) {
            result[0]["points_cost"] = pointCost;
        }
        return result;
    },
<<<<<<< HEAD
})
//092D4B
=======
})
>>>>>>> 39e3b2cd62c2de8883c30f05476d7023731c24ce
