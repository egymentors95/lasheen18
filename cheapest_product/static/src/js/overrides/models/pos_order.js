/** @odoo-module **/
/** (C) 2025 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com **/

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

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
        if (!discountable) {
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

        if (
            rewardAppliesTo === "order" &&
            ["per_point", "per_order"].includes(reward.discount_mode)
        ) {
            const rewardLineValues = [
                {
                    product_id: discountProduct,
                    price_unit: -Math.min(maxDiscount, discountable),
                    qty: 1,
                    reward_id: reward,
                    is_reward_line: true,
                    coupon_id: coupon_id,
                    points_cost: pointCost,
                    reward_identifier_code: rewardCode,
                    tax_ids: [],
                },
            ];

            let rewardTaxes = reward.tax_ids;
            if (rewardTaxes.length > 0) {
                if (this.fiscal_position_id) {
                    rewardTaxes = getTaxesAfterFiscalPosition(
                        rewardTaxes,
                        this.fiscal_position_id,
                        this.models
                    );
                }

                const matchingLines = this.get_orderlines().filter(
                    (line) =>
                        !line.is_delivery &&
                        line.tax_ids.length === rewardTaxes.length &&
                        line.tax_ids.every((tax_id) => rewardTaxes.includes(tax_id))
                );

                if (matchingLines.length == 0) {
                    return _t("No product is compatible with this promotion.");
                }

                const untaxedAmount = matchingLines.reduce(
                    (sum, line) => sum + line.get_price_without_tax(),
                    0
                );
                rewardLineValues[0].price_unit = Math.max(
                    -untaxedAmount,
                    rewardLineValues[0].price_unit
                );

                rewardLineValues[0].tax_ids = rewardTaxes;
            }
            if (Math.abs(rewardLineValues[0].price_unit) > this.amount_untaxed) {
                rewardLineValues[0].price_unit = -this.amount_untaxed;
            }
            return rewardLineValues;
        }

        const discountFactor = discountable ? Math.min(1, maxDiscount / discountable) : 1;
        const result = Object.entries(discountablePerTax).reduce((lst, entry) => {
            if (!entry[1]) {
                return lst;
            }
            let taxIds = entry[0] === "" ? [] : entry[0].split(",").map((str) => parseInt(str));
            taxIds = this.models["account.tax"].filter((tax) => taxIds.includes(tax.id));

            lst.push({
                product_id: discountProduct,
                product_id_ref: product_id_ref,
                price_unit: -(entry[1] * discountFactor),
                qty: 1,
                reward_id: reward,
                is_reward_line: true,
                coupon_id: coupon_id,
                points_cost: 0,
                reward_identifier_code: rewardCode,
                tax_ids: taxIds,
            });
            return lst;
        }, []);
        if (result.length) {
            result[0]["points_cost"] = pointCost;
        }
        return result;
    },
})
//092D4B
