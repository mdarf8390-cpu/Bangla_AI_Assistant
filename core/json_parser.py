"""
====================================================
AYESHA AI
JSON Parser V6 FIXED
====================================================
"""

from __future__ import annotations

import json
import re
from typing import Dict, Any



class JSONParser:


    REQUIRED_FIELDS = [
        "intent",
        "goal",
        "priority",
        "answer",
        "tasks"
    ]


    def clean(self,text:str):

        if not text:
            return ""

        text=text.strip()

        text=text.replace(
            "```json",
            ""
        )

        text=text.replace(
            "```",
            ""
        )

        return text.strip()



    def extract(self,text:str):

        text=self.clean(text)

        start=text.find("{")
        end=text.rfind("}")


        if start==-1 or end==-1:
            return ""


        return text[start:end+1]



    def parse(self,text:str):

        raw=self.extract(text)


        if not raw:
            return None


        try:

            data=json.loads(raw)

            return self.validate(data)


        except Exception:

            return self.repair(raw)



    def repair(self,text):

        try:

            text=re.sub(
                r",\s*}",
                "}",
                text
            )


            text=re.sub(
                r",\s*]",
                "]",
                text
            )


            data=json.loads(text)

            return self.validate(data)


        except Exception:

            return None



    def validate(self,data):

        if not isinstance(data,dict):

            return None


        for field in self.REQUIRED_FIELDS:

            if field not in data:

                if field=="priority":

                    data[field]=1

                elif field=="tasks":

                    data[field]=[]

                else:

                    data[field]=""



        return data



json_parser = JSONParser()