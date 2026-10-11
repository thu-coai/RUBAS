from BaseEnv import BaseEnv

class Payments(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.payments = []
        self.payment_counter = 1

    def create_alipay_payment(
        self,
        *,
        amount,
        subject,
        buyer_id,
        notify_url,
        currency="CNY",
        payment_method="BALANCE"
    ):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"success": False, "message": "Invalid amount."}
        if currency not in ["CNY", "USD", "JPY", "EUR", "GBP", "HKD", "CAD", "AUD"]:
            return {"success": False, "message": "Invalid currency."}
        if payment_method not in ["BALANCE", "BANK_CARD", "CREDIT_PAY"]:
            return {"success": False, "message": "Invalid payment method."}
        if not subject or not isinstance(subject, str):
            return {"success": False, "message": "Invalid subject."}
        if not buyer_id or not isinstance(buyer_id, str):
            return {"success": False, "message": "Invalid buyer_id."}
        if not notify_url or not isinstance(notify_url, str):
            return {"success": False, "message": "Invalid notify_url."}
        payment_id = f"alipay_{self.payment_counter}"
        self.payment_counter += 1
        payment = {
            "payment_id": payment_id,
            "type": "alipay",
            "amount": round(amount, 2),
            "currency": currency,
            "subject": subject,
            "buyer_id": buyer_id,
            "payment_method": payment_method,
            "notify_url": notify_url,
            "status": "PENDING"
        }
        self.payments.append(payment)
        return {"success": True, "data": {"payment_id": payment_id, "status": "PENDING"}}

    def query_alipay_payment(self, *, payment_id):
        for payment in self.payments:
            if payment["payment_id"] == payment_id and payment["type"] == "alipay":
                return {"success": True, "data": {"payment": payment}}
        return {"success": False, "message": "Payment not found."}

    def create_apple_pay_payment(
        self,
        *,
        amount,
        merchant_id,
        payment_data,
        line_items,
        currency="USD"
    ):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"success": False, "message": "Invalid amount."}
        if currency not in ["USD", "CNY", "JPY", "EUR", "GBP", "HKD", "CAD", "AUD"]:
            return {"success": False, "message": "Invalid currency."}
        if not merchant_id or not isinstance(merchant_id, str):
            return {"success": False, "message": "Invalid merchant_id."}
        if not isinstance(payment_data, dict) or "network" not in payment_data:
            return {"success": False, "message": "Invalid payment_data."}
        if payment_data["network"] not in ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]:
            return {"success": False, "message": "Invalid payment network."}
        if not isinstance(line_items, list) or not line_items:
            return {"success": False, "message": "Invalid line_items."}
        for item in line_items:
            if not isinstance(item, dict):
                return {"success": False, "message": "Invalid line item."}
            if "label" not in item or "amount" not in item:
                return {"success": False, "message": "Each line item must have label and amount."}
        payment_id = f"applepay_{self.payment_counter}"
        self.payment_counter += 1
        payment = {
            "payment_id": payment_id,
            "type": "apple_pay",
            "amount": round(amount, 2),
            "currency": currency,
            "merchant_id": merchant_id,
            "payment_data": payment_data,
            "line_items": line_items,
            "status": "PENDING"
        }
        self.payments.append(payment)
        return {"success": True, "data": {"payment_id": payment_id, "status": "PENDING"}}

    def query_apple_pay_payment(self, *, payment_id):
        for payment in self.payments:
            if payment["payment_id"] == payment_id and payment["type"] == "apple_pay":
                return {"success": True, "data": {"payment": payment}}
        return {"success": False, "message": "Payment not found."}

    def create_paypal_payment(
        self,
        *,
        amount,
        description,
        payer_email,
        return_url,
        cancel_url,
        items,
        currency="USD",
        intent="CAPTURE"
    ):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"success": False, "message": "Invalid amount."}
        if currency not in ["USD", "EUR", "GBP", "CAD", "AUD"]:
            return {"success": False, "message": "Invalid currency."}
        if intent not in ["CAPTURE", "AUTHORIZE"]:
            return {"success": False, "message": "Invalid intent."}
        if not description or not isinstance(description, str):
            return {"success": False, "message": "Invalid description."}
        if not payer_email or not isinstance(payer_email, str):
            return {"success": False, "message": "Invalid payer_email."}
        if not return_url or not isinstance(return_url, str):
            return {"success": False, "message": "Invalid return_url."}
        if not cancel_url or not isinstance(cancel_url, str):
            return {"success": False, "message": "Invalid cancel_url."}
        if not isinstance(items, list) or not items:
            return {"success": False, "message": "Invalid items."}
        for item in items:
            if not isinstance(item, dict):
                return {"success": False, "message": "Invalid item."}
            if "name" not in item or "quantity" not in item or "unit_amount" not in item:
                return {"success": False, "message": "Each item must have name, quantity, and unit_amount."}
        payment_id = f"paypal_{self.payment_counter}"
        self.payment_counter += 1
        payment = {
            "payment_id": payment_id,
            "type": "paypal",
            "amount": round(amount, 2),
            "currency": currency,
            "description": description,
            "intent": intent,
            "payer_email": payer_email,
            "return_url": return_url,
            "cancel_url": cancel_url,
            "items": items,
            "status": "PENDING"
        }
        self.payments.append(payment)
        return {"success": True, "data": {"payment_id": payment_id, "status": "PENDING"}}

    def query_paypal_payment(self, *, payment_id):
        for payment in self.payments:
            if payment["payment_id"] == payment_id and payment["type"] == "paypal":
                return {"success": True, "data": {"payment": payment}}
        return {"success": False, "message": "Payment not found."}

    def create_wechat_pay_payment(
        self,
        *,
        amount,
        description,
        openid,
        notify_url,
        currency="CNY",
        trade_type="NATIVE"
    ):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"success": False, "message": "Invalid amount."}
        if currency not in ["CNY", "USD", "HKD"]:
            return {"success": False, "message": "Invalid currency."}
        if trade_type not in ["NATIVE", "JSAPI", "H5", "APP"]:
            return {"success": False, "message": "Invalid trade_type."}
        if not description or not isinstance(description, str):
            return {"success": False, "message": "Invalid description."}
        if not openid or not isinstance(openid, str):
            return {"success": False, "message": "Invalid openid."}
        if not notify_url or not isinstance(notify_url, str):
            return {"success": False, "message": "Invalid notify_url."}
        payment_id = f"wechatpay_{self.payment_counter}"
        self.payment_counter += 1
        payment = {
            "payment_id": payment_id,
            "type": "wechat_pay",
            "amount": round(amount, 2),
            "currency": currency,
            "description": description,
            "trade_type": trade_type,
            "openid": openid,
            "notify_url": notify_url,
            "status": "PENDING"
        }
        self.payments.append(payment)
        return {"success": True, "data": {"payment_id": payment_id, "status": "PENDING"}}

    def query_wechat_pay_payment(self, *, payment_id):
        for payment in self.payments:
            if payment["payment_id"] == payment_id and payment["type"] == "wechat_pay":
                return {"success": True, "data": {"payment": payment}}
        return {"success": False, "message": "Payment not found."}

    def stripe_create_payment(
        self,
        *,
        amount,
        currency,
        payment_method_types,
        success_url,
        cancel_url,
        customer_email,
        description=None,
        metadata=None
    ):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"success": False, "message": "Invalid amount."}
        if not isinstance(currency, str) or len(currency) != 3 or not currency.isupper():
            return {"success": False, "message": "Invalid currency."}
        if not isinstance(payment_method_types, list) or not payment_method_types:
            return {"success": False, "message": "Invalid payment_method_types."}
        for method in payment_method_types:
            if method not in [
                "card",
                "alipay",
                "wechat_pay",
                "klarna",
                "afterpay_clearpay",
                "ideal"
            ]:
                return {"success": False, "message": f"Invalid payment method type: {method}."}
        if not success_url or not isinstance(success_url, str):
            return {"success": False, "message": "Invalid success_url."}
        if not cancel_url or not isinstance(cancel_url, str):
            return {"success": False, "message": "Invalid cancel_url."}
        if not customer_email or not isinstance(customer_email, str):
            return {"success": False, "message": "Invalid customer_email."}
        payment_id = f"stripe_{self.payment_counter}"
        self.payment_counter += 1
        payment = {
            "payment_id": payment_id,
            "type": "stripe",
            "amount": amount,
            "currency": currency,
            "payment_method_types": payment_method_types,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "customer_email": customer_email,
            "description": description,
            "metadata": metadata,
            "status": "PENDING"
        }
        self.payments.append(payment)
        return {
            "success": True,
            "data": {
                "payment_id": payment_id,
                "status": "PENDING",
                "payment_link": f"https://mock.stripe.com/pay/{payment_id}",
                "qr_code_url": f"https://mock.stripe.com/qr/{payment_id}"
            }
        }