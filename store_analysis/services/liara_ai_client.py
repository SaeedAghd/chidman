#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""مشترک: کلاینت ارتباط با سرویس Liara AI"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


logger = logging.getLogger(__name__)


class LiaraAIError(RuntimeError):
    """خطای عمومی هنگام ارتباط با Liara AI"""


@dataclass
class LiaraAIResponse:
    """نتیجه استاندارد از Liara"""

    model: str
    content: str
    raw: Dict[str, Any]

    def json(self) -> Dict[str, Any]:
        """تبدیل محتوا به JSON (با مدیریت خطا)"""
        try:
            return json.loads(self.content)
        except Exception as exc:  # pragma: no cover - خطای پارس به صورت کنترل‌شده
            raise LiaraAIError(f"خطا در پارس JSON پاسخ Liara: {exc}") from exc


class LiaraAIClient:
    """کلاینت ساده برای تماس با Liara AI"""

    def __init__(self) -> None:
        self.api_key: Optional[str] = os.getenv("LIARA_AI_API_KEY")
        # Liara AI endpoint - بر اساس مستندات رسمی
        # سرویس AI از طریق دامنه ai.liara.ir ارائه می‌شود
        # Endpoint صحیح: https://ai.liara.ir/api/{workspaceID}/v1/chat/completions
        base_url_raw = os.getenv(
            "LIARA_AI_BASE_URL", 
            "https://ai.liara.ir/api"  # Endpoint صحیح
        )
        
        # 🔧 اصلاح خودکار URL اشتباه (اگر از api.liara.ir استفاده شده باشد)
        if 'api.liara.ir' in base_url_raw:
            logger.warning(f"⚠️ URL قدیمی شناسایی شد: {base_url_raw} - در حال اصلاح به URL صحیح")
            # تبدیل api.liara.ir/v1 به ai.liara.ir/api
            base_url_raw = base_url_raw.replace('api.liara.ir/v1', 'ai.liara.ir/api')
            base_url_raw = base_url_raw.replace('api.liara.ir', 'ai.liara.ir/api')
            # حذف /v1 از انتها اگر وجود دارد
            if base_url_raw.endswith('/v1'):
                base_url_raw = base_url_raw[:-3]
            logger.info(f"✅ URL اصلاح شد به: {base_url_raw}")
        
        self.base_url: str = base_url_raw.rstrip('/')
        self.workspace_id: Optional[str] = os.getenv("LIARA_AI_PROJECT_ID", "ai-vmqbcxnig")
        self.session = requests.Session()
        self.timeout: int = int(os.getenv("LIARA_AI_TIMEOUT", "90"))  # 90 ثانیه برای production
        
        # تنظیمات session برای performance بهتر
        self.session.headers.update({
            'User-Agent': 'Chidmano-AI-Client/1.0',
        })

        if not self.api_key:
            logger.warning("⚠️ متغیر LIARA_AI_API_KEY تنظیم نشده است؛ از fallback استفاده می‌شود.")
        else:
            logger.info(f"✅ LiaraAIClient initialized with endpoint: {self.base_url}, workspace_id: {self.workspace_id}")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def chat(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_output_tokens: int = 4096,
        response_format: Optional[str] = "json_object",
    ) -> LiaraAIResponse:
        if not self.api_key:
            raise LiaraAIError("LIARA_AI_API_KEY تعریف نشده است")

        # ساخت URL صحیح: https://ai.liara.ir/api/{workspaceID}/v1/chat/completions
        if not self.workspace_id:
            raise LiaraAIError("LIARA_AI_PROJECT_ID (workspaceID) تعریف نشده است")
        
        url = f"{self.base_url.rstrip('/')}/{self.workspace_id}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "model": model,
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        if response_format == "json_object":
            payload["response_format"] = {"type": "json_object"}

        try:
            logger.info(f"🚀 ارسال درخواست به Liara AI (model={model}, url={url})")
            response = self.session.post(
                url, 
                json=payload, 
                headers=headers, 
                timeout=self.timeout
            )
        except requests.Timeout as exc:
            logger.error(f"⏱️ Timeout در ارتباط با Liara AI بعد از {self.timeout} ثانیه")
            raise LiaraAIError(f"Timeout در ارتباط با Liara AI: {exc}") from exc
        except requests.ConnectionError as exc:
            logger.error(f"🔌 خطای اتصال به Liara AI: {exc}")
            raise LiaraAIError(f"عدم دسترسی به Liara AI (اتصال): {exc}") from exc
        except requests.RequestException as exc:  # pragma: no cover - خطای شبکه
            logger.error(f"❌ خطای شبکه در ارتباط با Liara AI: {exc}")
            raise LiaraAIError(f"عدم دسترسی به Liara AI: {exc}") from exc

        # بررسی status code
        if response.status_code == 401:
            logger.error("🔐 خطای احراز هویت: API key نامعتبر است")
            raise LiaraAIError("API key نامعتبر است یا منقضی شده")
        elif response.status_code == 429:
            logger.warning("⏸ Rate limit: درخواست‌ها زیاد است، لطفاً صبر کنید")
            raise LiaraAIError("Rate limit: تعداد درخواست‌ها بیش از حد مجاز است")
        elif response.status_code >= 400:
            error_text = response.text[:500]  # افزایش طول برای debugging بهتر
            logger.error(f"❌ پاسخ ناموفق Liara AI (status={response.status_code}): {error_text}")
            raise LiaraAIError(
                f"پاسخ ناموفق Liara AI (status={response.status_code}): {error_text}"
            )

        # پارس JSON response
        try:
            data = response.json()
        except ValueError as json_exc:
            logger.error(f"❌ خطا در پارس JSON پاسخ: {response.text[:200]}")
            raise LiaraAIError(f"پاسخ Liara AI فرمت JSON معتبری ندارد: {json_exc}") from json_exc
        
        # استخراج content
        try:
            choices = data.get("choices", [])
            if not choices:
                raise LiaraAIError(f"پاسخ Liara AI شامل choices نیست: {data}")
            content = choices[0].get("message", {}).get("content", "")
            if not content:
                raise LiaraAIError(f"محتوای پاسخ Liara AI خالی است: {data}")
        except (KeyError, IndexError) as exc:
            logger.error(f"❌ ساختار پاسخ Liara نامعتبر است: {data}")
            raise LiaraAIError(f"ساختار پاسخ Liara نامعتبر است: {data}") from exc

        logger.info(f"✅ پاسخ Liara AI دریافت شد با مدل {model} (length={len(content)} chars)")
        return LiaraAIResponse(model=model, content=content, raw=data)

