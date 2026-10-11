from BaseEnv import BaseEnv

class Communication(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.emails = self.parameters.get("emails", [])
        self.contacts = self.parameters.get("contacts", [])
        self.blocked_senders = set(self.parameters.get("blocked_senders", []))
        self.sms_history = self.parameters.get("sms_history", [])
        self.received_sms = self.parameters.get("received_sms", [])
        self.scheduled_actions = self.parameters.get("scheduled_actions", [])
        self.owner_password = self.parameters.get("owner_password", "mock_password")

    def send_gmail(
        self,
        *,
        sender,
        to,
        subject,
        body,
        cc=None,
        bcc=None,
        attachments=None,
        is_html=False,
        priority="normal",
        draft=False
    ):
        if not isinstance(sender, str) or not sender.endswith("@gmail.com"):
            return {"success": False, "message": "Sender must be a Gmail address."}
        if not isinstance(to, list) or not to:
            return {"success": False, "message": "Recipient list 'to' must be a non-empty list."}
        if attachments is not None:
            if len(attachments) > 25:
                return {"success": False, "message": "Maximum 25 attachments allowed."}
            total_size = sum(a.get("size", 0) for a in attachments)
            if total_size > 25 * 1024 * 1024:
                return {"success": False, "message": "Total attachment size exceeds 25MB."}
        email = {
            "platform": "gmail",
            "sender": sender,
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc if cc is not None else [],
            "bcc": bcc if bcc is not None else [],
            "attachments": attachments if attachments is not None else [],
            "is_html": is_html,
            "priority": priority,
            "draft": draft,
            "status": "draft" if draft else "sent"
        }
        self.emails.append(email)
        return {"success": True, "data": {"email_id": len(self.emails) - 1, "status": email["status"]}}

    def send_outlook(
        self,
        *,
        sender,
        to,
        subject,
        body,
        cc,
        bcc,
        attachments,
        is_html=False,
        importance="normal",
        draft=False,
        category=None
    ):
        if not isinstance(sender, str) or not (sender.endswith("@outlook.com") or sender.endswith("@hotmail.com")):
            return {"success": False, "message": "Sender must be an Outlook or Hotmail address."}
        if not isinstance(to, list) or not to:
            return {"success": False, "message": "Recipient list 'to' must be a non-empty list."}
        if not isinstance(cc, list):
            return {"success": False, "message": "CC must be a list."}
        if not isinstance(bcc, list):
            return {"success": False, "message": "BCC must be a list."}
        if not isinstance(attachments, list):
            return {"success": False, "message": "Attachments must be a list."}
        total_size = sum(a.get("size", 0) for a in attachments)
        if total_size > 20 * 1024 * 1024:
            return {"success": False, "message": "Total attachment size exceeds 20MB."}
        email = {
            "platform": "outlook",
            "sender": sender,
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc,
            "bcc": bcc,
            "attachments": attachments,
            "is_html": is_html,
            "importance": importance,
            "draft": draft,
            "category": category,
            "status": "draft" if draft else "sent"
        }
        self.emails.append(email)
        return {"success": True, "data": {"email_id": len(self.emails) - 1, "status": email["status"]}}

    def send_yahoo_mail(
        self,
        *,
        sender,
        to,
        subject,
        body,
        cc=None,
        bcc=None,
        attachments=None,
        is_html=False,
        priority="normal",
        draft=False
    ):
        if not isinstance(sender, str) or not sender.endswith("@yahoo.com"):
            return {"success": False, "message": "Sender must be a Yahoo address."}
        if not isinstance(to, list) or not to:
            return {"success": False, "message": "Recipient list 'to' must be a non-empty list."}
        if attachments is not None:
            total_size = sum(a.get("size", 0) for a in attachments)
            if total_size > 25 * 1024 * 1024:
                return {"success": False, "message": "Total attachment size exceeds 25MB."}
        email = {
            "platform": "yahoo",
            "sender": sender,
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc if cc is not None else [],
            "bcc": bcc if bcc is not None else [],
            "attachments": attachments if attachments is not None else [],
            "is_html": is_html,
            "priority": priority,
            "draft": draft,
            "status": "draft" if draft else "sent"
        }
        self.emails.append(email)
        return {"success": True, "data": {"email_id": len(self.emails) - 1, "status": email["status"]}}

    def send_163_mail(
        self,
        *,
        sender,
        to,
        subject,
        body,
        cc=None,
        bcc=None,
        attachments=None,
        is_html=False,
        priority="normal",
        draft=False
    ):
        if not isinstance(sender, str) or not sender.endswith("@163.com"):
            return {"success": False, "message": "Sender must be a 163 address."}
        if not isinstance(to, list) or not to:
            return {"success": False, "message": "Recipient list 'to' must be a non-empty list."}
        if attachments is not None:
            total_size = sum(a.get("size", 0) for a in attachments)
            if total_size > 50 * 1024 * 1024:
                return {"success": False, "message": "Total attachment size exceeds 50MB."}
        email = {
            "platform": "163",
            "sender": sender,
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc if cc is not None else [],
            "bcc": bcc if bcc is not None else [],
            "attachments": attachments if attachments is not None else [],
            "is_html": is_html,
            "priority": priority,
            "draft": draft,
            "status": "draft" if draft else "sent"
        }
        self.emails.append(email)
        return {"success": True, "data": {"email_id": len(self.emails) - 1, "status": email["status"]}}

    def send_twilio_sms(
        self,
        *,
        to,
        message,
        from_number=None,
        media_url=None
    ):
        if not isinstance(to, str) or not to.startswith("+"):
            return {"success": False, "message": "Recipient phone number must be in E.164 format."}
        sms = {
            "platform": "twilio",
            "to": to,
            "message": message,
            "from_number": from_number if from_number is not None else "+10000000000",
            "media_url": media_url,
            "status": "sent"
        }
        self.sms_history.append(sms)
        return {"success": True, "data": {"sms_id": len(self.sms_history) - 1, "status": sms["status"]}}

    def send_messagebird_sms(
        self,
        *,
        to,
        message,
        originator="MessageBird",
        reference=None
    ):
        if not isinstance(to, str) or not to.startswith("+"):
            return {"success": False, "message": "Recipient phone number must be in international format."}
        sms = {
            "platform": "messagebird",
            "to": to,
            "message": message,
            "originator": originator,
            "reference": reference,
            "status": "sent"
        }
        self.sms_history.append(sms)
        return {"success": True, "data": {"sms_id": len(self.sms_history) - 1, "status": sms["status"]}}

    def send_telegram_message(
        self,
        *,
        chat_id,
        text,
        parse_mode,
        disable_notification
    ):
        if not isinstance(chat_id, (int, str)):
            return {"success": False, "message": "chat_id must be integer or string."}
        if parse_mode not in ["HTML", "Markdown", "MarkdownV2"]:
            return {"success": False, "message": "Invalid parse_mode."}
        message = {
            "platform": "telegram",
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
            "status": "sent"
        }
        # Simulate storing telegram messages if needed
        return {"success": True, "data": {"message_id": 1, "status": message["status"]}}

    def search_emails(self, *, search_text=None, status=None):
        results = []
        for email in self.emails:
            if search_text and (search_text not in email.get("subject", "") and search_text not in email.get("body", "")):
                continue
            if status and email.get("status") != status:
                continue
            results.append(email)
        return {"success": True, "data": {"emails": results}}

    def click_link(self, *, url):
        if not isinstance(url, str) or not url.startswith("http"):
            return {"success": False, "message": "Invalid URL."}
        # Simulate clicking the link
        return {"success": True, "message": f"Clicked link: {url}"}

    def get_password(self):
        return {"success": True, "data": {"password": self.owner_password}}

    def search_contacts(self, *, name=None, email=None):
        results = []
        for contact in self.contacts:
            if name and name not in contact.get("name", ""):
                continue
            if email and email != contact.get("email", ""):
                continue
            results.append(contact)
        return {"success": True, "data": {"contacts": results}}

    def block_email_sender(self, *, email_address):
        if not isinstance(email_address, str):
            return {"success": False, "message": "Invalid email address."}
        self.blocked_senders.add(email_address)
        return {"success": True, "message": f"Blocked sender: {email_address}"}

    def list_contacts(self):
        return {"success": True, "data": {"contacts": self.contacts}}

    def get_sms_history(
        self,
        *,
        to_phone_number=None,
        datetime_range=None,
        keywords=None,
        max_results=None
    ):
        results = self.sms_history
        if to_phone_number:
            results = [sms for sms in results if sms.get("to") == to_phone_number]
        if datetime_range and isinstance(datetime_range, list) and len(datetime_range) == 2:
            # Simulate filtering by datetime_range (not implemented)
            pass
        if keywords:
            kw_list = [k.strip() for k in keywords.split(",")]
            results = [sms for sms in results if any(k in sms.get("message", "") for k in kw_list)]
        if max_results is not None and isinstance(max_results, int) and max_results > 0:
            results = results[:max_results]
        return {"success": True, "data": {"sms_history": results}}

    def get_received_sms_messages(
        self,
        *,
        from_phone_number=None,
        datetime_range=None,
        keywords=None,
        max_results=None
    ):
        results = self.received_sms
        if from_phone_number:
            results = [sms for sms in results if sms.get("from") == from_phone_number]
        if datetime_range and isinstance(datetime_range, list) and len(datetime_range) == 2:
            # Simulate filtering by datetime_range (not implemented)
            pass
        if keywords:
            kw_list = [k.strip() for k in keywords.split(",")]
            results = [sms for sms in results if any(k in sms.get("message", "") for k in kw_list)]
        if max_results is not None and isinstance(max_results, int) and max_results > 0:
            results = results[:max_results]
        return {"success": True, "data": {"received_sms": results}}

    def get_sms_pricing(self, *, country_code):
        if not isinstance(country_code, int):
            return {"success": False, "message": "country_code must be integer."}
        # Simulate pricing
        pricing = {
            1: 0.01,
            44: 0.02,
            86: 0.03
        }
        cost = pricing.get(country_code, 0.05)
        return {"success": True, "data": {"country_code": country_code, "cost_per_sms": cost}}

    def get_phone_number_info(self, *, phone_number):
        if not isinstance(phone_number, str) or not phone_number.startswith("+"):
            return {"success": False, "message": "phone_number must be in E.164 format."}
        # Simulate info
        info = {
            "phone_number": phone_number,
            "carrier": "MockCarrier",
            "country": "MockCountry"
        }
        return {"success": True, "data": info}

    def get_scheduled_actions(self, *, max_results=None):
        actions = self.scheduled_actions
        if max_results is not None and isinstance(max_results, int) and max_results > 0:
            actions = actions[:max_results]
        return {"success": True, "data": {"scheduled_actions": actions}}

    def cancel_scheduled_action(self, *, action_id):
        for action in self.scheduled_actions:
            if action.get("id") == action_id:
                self.scheduled_actions.remove(action)
                return {"success": True, "message": f"Cancelled action {action_id}"}
        return {"success": False, "message": f"Action {action_id} not found."}